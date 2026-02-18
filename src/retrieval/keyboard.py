"""KeyboardNavigator — all Discord key sequences.

Guards at import time: raises ImportError on non-Windows.
Does NOT hold a reference to ClipboardReader (clean separation).
"""
from __future__ import annotations

import sys

if sys.platform != "win32":
    raise ImportError("pywinauto requires Windows. Use scripts/run_retrieval.bat.")

import time

from pywinauto.keyboard import send_keys  # type: ignore[import-untyped]

# Discord keyboard shortcut constants (pywinauto send_keys format)
KEY_QUICKSWITCHER = "^k"   # Ctrl+K  — open Quick Switcher
KEY_COPY = "^c"            # Ctrl+C  — copy focused message
KEY_ESCAPE = "{ESC}"       # Escape  — dismiss overlay / reset focus
KEY_ENTER = "{ENTER}"      # Enter   — confirm Quick Switcher selection
KEY_END = "{END}"          # End     — jump to bottom of channel
KEY_DOWN = "{DOWN}"        # Down    — anchor at the newest message
KEY_UP = "{UP}"            # Up      — move to the next older message


class KeyboardNavigator:
    """Sends keyboard sequences to Discord to navigate and copy messages.

    All timing delays are configurable via the constructor.
    Never interacts with the clipboard directly.
    """

    def __init__(
        self,
        quickswitcher_delay: float = 1.0,
        navigation_delay: float = 0.3,
        post_channel_nav_delay: float = 2.0,
    ) -> None:
        self._quickswitcher_delay = quickswitcher_delay
        self._navigation_delay = navigation_delay
        self._post_channel_nav_delay = post_channel_nav_delay

    def navigate_to_channel(self, channel_name: str) -> None:
        """Open Quick Switcher, type the channel name, confirm, and settle."""
        send_keys(KEY_QUICKSWITCHER)
        time.sleep(self._quickswitcher_delay)
        # with_spaces=True prevents '{' and '}' from being treated as special
        send_keys(channel_name, with_spaces=True)
        time.sleep(self._quickswitcher_delay)
        send_keys(KEY_ENTER)
        time.sleep(self._post_channel_nav_delay)

    def move_to_newest_message(self) -> None:
        """Jump to the bottom of the channel and anchor on the newest message."""
        send_keys(KEY_END)
        time.sleep(self._navigation_delay)
        send_keys(KEY_DOWN)
        time.sleep(self._navigation_delay)

    def move_up(self) -> None:
        """Move focus to the next older message."""
        send_keys(KEY_UP)
        time.sleep(self._navigation_delay)

    def copy_focused_message(self) -> None:
        """Send Ctrl+C to copy the currently focused message text.

        Clipboard read is the caller's responsibility (via ClipboardReader).
        """
        send_keys(KEY_COPY)

    def dismiss_overlay(self) -> None:
        """Press Escape to dismiss any overlay or reset Discord focus."""
        send_keys(KEY_ESCAPE)
        time.sleep(self._navigation_delay)
