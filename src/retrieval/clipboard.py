"""ClipboardReader — read clipboard with retry and exponential backoff."""
from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    class pyperclip:  # noqa: N801
        @staticmethod
        def copy(text: str) -> None: ...
        @staticmethod
        def paste() -> str: ...
else:
    import pyperclip  # type: ignore[import-untyped]

from .errors import ClipboardTimeoutError


class ClipboardReader:
    """Reads the system clipboard, retrying with exponential backoff.

    Designed to be used around Discord's Ctrl+C keyboard shortcut:
    1. Caller calls clear() before triggering the copy.
    2. Caller triggers the copy (Ctrl+C via KeyboardNavigator).
    3. Caller calls read_with_retry() to get the text.
    """

    def __init__(
        self,
        retries: int = 3,
        settle_delay: float = 0.15,
        initial_backoff: float = 0.2,
    ) -> None:
        self._retries = retries
        self._settle_delay = settle_delay
        self._initial_backoff = initial_backoff

    def clear(self) -> None:
        """Empty the clipboard before a copy operation."""
        pyperclip.copy("")

    def read_with_retry(self, nav_index: int) -> tuple[str, int]:
        """Wait for non-empty clipboard content, retrying with backoff.

        Returns:
            (text, attempt_count) where attempt_count is 1-based.

        Raises:
            ClipboardTimeoutError: all retries exhausted with empty clipboard.
        """
        time.sleep(self._settle_delay)
        backoff = self._initial_backoff
        for attempt in range(self._retries):
            text: str = pyperclip.paste()
            if text:
                return text, attempt + 1
            if attempt < self._retries - 1:
                time.sleep(backoff)
                backoff *= 2
        raise ClipboardTimeoutError(
            f"Clipboard empty after {self._retries} attempts",
            {"nav_index": nav_index, "attempts": self._retries},
        )
