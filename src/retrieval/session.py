"""RetrievalSession — orchestrator for keyboard-driven Discord message retrieval.

Mirrors the ScrapeOrchestrator pattern from src/domain/scrape-engine/ScrapeOrchestrator.ts.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .clipboard import ClipboardReader
from .config import RetrievalConfig
from .errors import (
    ClipboardTimeoutError,
    NavigationError,
    NavigationStuckError,
    SessionError,
    WindowError,
)
from .keyboard import KeyboardNavigator
from .logger import ComponentLogger
from .metadata import MessageMetadataExtractor
from .models import MessageRecord
from .window import WindowManager

_STUCK_THRESHOLD = 3  # consecutive identical clipboard hashes before declaring stuck


@dataclass
class SessionResult:
    """Return value of RetrievalSession.execute()."""

    session_id: str
    channel_name: str
    records: list[MessageRecord] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    completed: bool = False


class RetrievalSession:
    """Coordinates window focus, keyboard navigation, clipboard capture, and UIA metadata.

    Constructor validates config and wires all dependencies.
    Call execute() to run the full retrieval loop.
    """

    def __init__(self, config: RetrievalConfig) -> None:
        self._config = config
        self._session_id = str(uuid.uuid4())
        self._log = ComponentLogger(
            "retrieval.session",
            config.log_level,
            config.log_dir,
        )
        self._window = WindowManager()
        self._keyboard = KeyboardNavigator(
            quickswitcher_delay=config.quickswitcher_delay,
            navigation_delay=config.navigation_delay,
            post_channel_nav_delay=config.post_channel_nav_delay,
        )
        self._clipboard = ClipboardReader(
            retries=config.clipboard_retries,
            settle_delay=config.copy_settle_delay,
            initial_backoff=config.clipboard_retry_backoff,
        )
        self._metadata_extractor = MessageMetadataExtractor()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(self) -> SessionResult:
        """Run the full retrieval loop and return a SessionResult.

        Fatal errors (WindowError, NavigationError) are wrapped in SessionError
        and re-raised. Non-fatal per-message errors are recorded in result.errors.
        """
        result = SessionResult(
            session_id=self._session_id,
            channel_name=self._config.channel_name,
        )
        self._log.info("Session starting", {
            "session_id": self._session_id,
            "channel": self._config.channel_name,
            "message_count": self._config.message_count,
        })
        try:
            self._setup()
            self._run_loop(result)
            result.completed = True
            self._log.info("Session completed", {
                "session_id": self._session_id,
                "records": len(result.records),
                "errors": len(result.errors),
            })
        except (WindowError, NavigationError) as exc:
            self._log.error("Session aborted (fatal)", {
                "session_id": self._session_id,
                "error": str(exc),
                "context": exc.context,
            })
            raise SessionError(str(exc), {"cause": str(exc)}) from exc
        except Exception as exc:
            self._log.error("Session aborted (unexpected)", {
                "session_id": self._session_id,
                "error": str(exc),
            })
            raise SessionError(f"Unexpected error: {exc}", {}) from exc
        finally:
            self._cleanup(result)
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        """Connect to Discord, focus the window, and navigate to the channel."""
        self._window.connect(title_re=r"Discord.*")
        self._log.info("Discord window found", {"title": self._window.title})
        self._window.focus(self._config.focus_delay)

        self._keyboard.navigate_to_channel(self._config.channel_name)
        self._log.info("Navigated to channel", {"channel": self._config.channel_name})

        self._keyboard.move_to_newest_message()
        time.sleep(self._config.navigation_delay)

    def _run_loop(self, result: SessionResult) -> None:
        """Main retrieval loop: capture message_count messages newest→oldest."""
        last_hash = ""
        consecutive_same = 0
        stuck_recovery_attempted = False

        for nav_index in range(self._config.message_count):
            # --- Copy ---
            self._clipboard.clear()
            self._keyboard.copy_focused_message()

            try:
                raw_text, attempt_count = self._clipboard.read_with_retry(nav_index)
            except ClipboardTimeoutError as exc:
                self._log.error("Clipboard timeout", {
                    "nav_index": nav_index,
                    "error": str(exc),
                })
                result.errors.append({"nav_index": nav_index, "error": str(exc)})
                self._keyboard.move_up()
                continue

            # --- Stuck detection ---
            current_hash = hashlib.md5(raw_text.encode()).hexdigest()
            if current_hash == last_hash:
                consecutive_same += 1
            else:
                consecutive_same = 0
                last_hash = current_hash

            if consecutive_same >= _STUCK_THRESHOLD:
                if stuck_recovery_attempted:
                    raise NavigationStuckError(
                        "Still stuck after recovery attempt",
                        {"nav_index": nav_index, "consecutive_same": consecutive_same},
                    )
                self._log.warn("Navigation stuck, attempting recovery", {
                    "nav_index": nav_index,
                    "consecutive_same": consecutive_same,
                })
                self._keyboard.dismiss_overlay()
                self._window.focus(self._config.focus_delay)
                stuck_recovery_attempted = True
                consecutive_same = 0
                last_hash = ""
                continue  # retry this nav_index position without move_up

            # --- UIA metadata ---
            time.sleep(self._config.metadata_delay)
            focused_element = self._window.get_focused_element()
            raw_meta = self._metadata_extractor.extract(focused_element)

            if raw_meta.extraction_succeeded:
                self._log.debug("UIA metadata extracted", {
                    "nav_index": nav_index,
                    "author": raw_meta.author,
                    "is_reply": raw_meta.is_reply,
                    "discord_timestamp": raw_meta.discord_timestamp,
                })
            else:
                self._log.warn("UIA metadata extraction failed", {
                    "nav_index": nav_index,
                    "error": "extraction_succeeded=False",
                    "uia_name": raw_meta.uia_name,
                })

            # --- Assemble record ---
            record = MessageRecord(
                raw_text=raw_text,
                captured_at=datetime.now(UTC),
                nav_index=nav_index,
                channel_name=self._config.channel_name,
                session_id=self._session_id,
                author=raw_meta.author,
                discord_timestamp=raw_meta.discord_timestamp,
                is_reply=raw_meta.is_reply,
                reply_to_author=raw_meta.reply_to_author,
                metadata_extraction_succeeded=raw_meta.extraction_succeeded,
                copy_attempt_count=attempt_count,
            )
            result.records.append(record)

            self._keyboard.move_up()

    def _cleanup(self, result: SessionResult) -> None:
        """Write output JSONL and close logger. Always called via finally."""
        if result.records:
            self._write_output(result)
        self._log.close()

    def _write_output(self, result: SessionResult) -> None:
        """Write all captured records to a JSONL file under output_dir."""
        output_dir = Path(self._config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        safe_channel = self._config.channel_name.replace("/", "-").replace("\\", "-")
        output_path = output_dir / f"retrieval-{safe_channel}-{ts}.jsonl"
        with open(output_path, "w", encoding="utf-8") as f:
            for record in result.records:
                f.write(json.dumps(record.to_dict()) + "\n")
        self._log.info("Output written", {
            "path": str(output_path),
            "records": len(result.records),
        })
