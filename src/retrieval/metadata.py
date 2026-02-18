"""MessageMetadataExtractor — targeted UIA read on focused element only.

Guards at import time: raises ImportError on non-Windows.
Never walks the full element tree — one element, depth-1 children, targeted
property reads only. Never raises; degrades gracefully to extraction_succeeded=False.
"""
from __future__ import annotations

import sys

if sys.platform != "win32":
    raise ImportError("pywinauto requires Windows. Use scripts/run_retrieval.bat.")

from dataclasses import dataclass
from typing import Any


@dataclass
class RawMetadata:
    """Structured metadata extracted from a single focused UIA element."""

    author: str | None
    discord_timestamp: str | None  # raw string from UIA, e.g. "Today at 3:45 PM"
    is_reply: bool
    reply_to_author: str | None    # populated from "Replying to @username" child
    uia_name: str | None           # raw UIA Name property (for debug logging)
    extraction_succeeded: bool


_FAILED = RawMetadata(
    author=None,
    discord_timestamp=None,
    is_reply=False,
    reply_to_author=None,
    uia_name=None,
    extraction_succeeded=False,
)


class MessageMetadataExtractor:
    """Reads a single UIA element to extract Discord message metadata.

    Usage:
        element = window_manager.get_focused_element()
        meta = extractor.extract(element)
    """

    def extract(self, focused_element: Any) -> RawMetadata:
        """Extract metadata from the focused element. Never raises."""
        if focused_element is None:
            return _FAILED
        try:
            return self._do_extract(focused_element)
        except Exception:
            return _FAILED

    def _do_extract(self, element: Any) -> RawMetadata:
        uia_name: str | None = None
        author: str | None = None
        discord_timestamp: str | None = None
        is_reply = False
        reply_to_author: str | None = None

        # --- UIA Name (primary text label) ---
        try:
            raw = element.window_text()
            uia_name = str(raw) if raw else None
        except Exception:
            pass

        # --- HelpText → timestamp ---
        try:
            info = element.element_info
            if hasattr(info, "help_text") and info.help_text:
                discord_timestamp = str(info.help_text)
        except Exception:
            pass

        # --- Parse author from Name ---
        # Discord's UIA Name for a message is typically:
        #   "AuthorName, message content, timestamp" or similar
        if uia_name:
            parts = uia_name.split(", ", 1)
            if parts[0].strip():
                author = parts[0].strip()

        # --- Scan depth-1 children for reply indicator and timestamp fallback ---
        try:
            children: list[Any] = list(element.children())
            for child in children:
                try:
                    child_name: str = str(child.window_text() or "")
                    if child_name.startswith("Replying to"):
                        is_reply = True
                        # "Replying to @username" → "@username"
                        words = child_name.split(" ", 2)
                        if len(words) >= 3:
                            reply_to_author = words[2].strip() or None
                    elif discord_timestamp is None and child_name:
                        # Fallback: first non-empty child text might be a timestamp
                        # (only if HelpText was unavailable)
                        pass  # intentionally conservative — don't guess
                except Exception:
                    continue
        except Exception:
            pass

        return RawMetadata(
            author=author,
            discord_timestamp=discord_timestamp,
            is_reply=is_reply,
            reply_to_author=reply_to_author,
            uia_name=uia_name,
            extraction_succeeded=True,
        )
