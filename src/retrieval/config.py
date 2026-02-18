"""Configuration dataclass for the retrieval subsystem."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetrievalConfig:
    """All tunable parameters for a RetrievalSession.

    Required fields must be supplied by the caller; all others have
    sensible defaults tuned for typical Discord desktop latency.
    """

    # Required
    channel_name: str
    message_count: int

    # Window / focus
    focus_delay: float = 0.5

    # Quick Switcher navigation
    quickswitcher_delay: float = 1.0
    post_channel_nav_delay: float = 2.0

    # Per-message navigation
    navigation_delay: float = 0.3

    # Clipboard
    copy_settle_delay: float = 0.15
    clipboard_retries: int = 3
    clipboard_retry_backoff: float = 0.2  # seconds; doubles each failure

    # UIA metadata
    metadata_delay: float = 0.1  # pause before UIA read after focus settles

    # Output
    output_dir: str = "data/retrieval"
    log_dir: str = "data/logs"
    log_level: str = "info"
