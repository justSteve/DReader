"""Custom exception hierarchy for the DReader retrieval subsystem."""
from __future__ import annotations

from typing import Any


class DReaderError(Exception):
    """Base exception for all DReader errors. Always carries a context dict."""

    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.context: dict[str, Any] = context or {}


class WindowError(DReaderError):
    """Errors related to the Discord window."""


class WindowNotFoundError(WindowError):
    """Discord application window not found (not running)."""


class WindowFocusError(WindowError):
    """Discord window found but could not be focused."""


class NavigationError(DReaderError):
    """Errors during in-Discord keyboard navigation."""


class ChannelNotFoundError(NavigationError):
    """Quick Switcher + channel name + Enter did not land on the channel."""


class NavigationStuckError(NavigationError):
    """Same clipboard content seen N consecutive times — navigation is frozen."""


class ClipboardError(DReaderError):
    """Errors related to clipboard read/write operations."""


class ClipboardEmptyError(ClipboardError):
    """Single empty clipboard read (informational — not raised externally)."""


class ClipboardTimeoutError(ClipboardError):
    """All clipboard retry attempts exhausted (non-fatal per message)."""


class MetadataError(DReaderError):
    """UIA metadata access failed — always non-fatal, logged only."""


class SessionError(DReaderError):
    """Wraps any fatal abort of a RetrievalSession."""
