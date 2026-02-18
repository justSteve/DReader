"""DReader retrieval subsystem — keyboard-driven Discord message capture.

Platform-safe exports only. Window/keyboard/session modules require Windows.
"""
from __future__ import annotations

from .config import RetrievalConfig
from .errors import (
    ChannelNotFoundError,
    ClipboardTimeoutError,
    DReaderError,
    NavigationStuckError,
    SessionError,
    WindowFocusError,
    WindowNotFoundError,
)
from .models import MessageRecord

__all__ = [
    "RetrievalConfig",
    "MessageRecord",
    "DReaderError",
    "WindowNotFoundError",
    "WindowFocusError",
    "ChannelNotFoundError",
    "NavigationStuckError",
    "ClipboardTimeoutError",
    "SessionError",
]
