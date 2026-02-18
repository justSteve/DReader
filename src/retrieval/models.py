"""Data models for captured Discord messages."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


def _fmt_dt(dt: datetime) -> str:
    """Format datetime as JS-compatible ISO string: 2026-02-18T12:00:00.000Z"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


@dataclass(frozen=True)
class MessageRecord:
    """A single captured Discord message, fully typed and immutable."""

    # Always populated (clipboard path)
    raw_text: str
    captured_at: datetime  # UTC, our clock
    nav_index: int  # 0 = newest message, increases toward older
    channel_name: str  # from config
    session_id: str

    # Populated via UIA metadata extraction (None if extraction failed)
    author: str | None
    discord_timestamp: str | None  # raw string, e.g. "Today at 3:45 PM"
    is_reply: bool
    reply_to_author: str | None  # extracted from "Replying to @username"

    # Diagnostics
    metadata_extraction_succeeded: bool
    copy_attempt_count: int

    def to_dict(self) -> dict[str, object]:
        """Serialize to a JSON-compatible dict for JSONL output."""
        return {
            "raw_text": self.raw_text,
            "captured_at": _fmt_dt(self.captured_at),
            "nav_index": self.nav_index,
            "channel_name": self.channel_name,
            "session_id": self.session_id,
            "author": self.author,
            "discord_timestamp": self.discord_timestamp,
            "is_reply": self.is_reply,
            "reply_to_author": self.reply_to_author,
            "metadata_extraction_succeeded": self.metadata_extraction_succeeded,
            "copy_attempt_count": self.copy_attempt_count,
        }
