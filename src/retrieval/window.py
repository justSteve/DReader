"""WindowManager — pywinauto connect/focus/focused-element only.

Guards at import time: raises ImportError on non-Windows.
All pywinauto usage is confined to this module.
"""
from __future__ import annotations

import sys
import time
from typing import TYPE_CHECKING, Any

if not TYPE_CHECKING and sys.platform != "win32":
    raise ImportError("pywinauto requires Windows. Use scripts/run_retrieval.bat.")

if TYPE_CHECKING:
    class _PywinautoApp:
        def connect(self, **kwargs: object) -> Any: ...
        def top_window(self) -> Any: ...
    class pywinauto:  # noqa: N801
        @staticmethod
        def Application(backend: str) -> _PywinautoApp: ...  # noqa: N802
else:
    import pywinauto  # type: ignore[import-untyped]

from .errors import WindowFocusError, WindowNotFoundError


class WindowManager:
    """Thin wrapper around pywinauto for connect, focus, and focused-element query.

    Never walks the full element tree — only connect, set_focus, and a
    single-element focus query are performed.
    """

    def __init__(self) -> None:
        self._app: Any = None
        self._window: Any = None

    def connect(self, title_re: str) -> None:
        """Connect to a running application whose window title matches title_re.

        Raises:
            WindowNotFoundError: no matching window found.
        """
        try:
            self._app = pywinauto.Application(backend="uia").connect(title_re=title_re)
            self._window = self._app.top_window()
        except Exception as exc:
            raise WindowNotFoundError(
                f"Discord window not found: {title_re!r}",
                {"title_re": title_re},
            ) from exc

    def focus(self, delay: float = 0.5) -> None:
        """Bring the Discord window to the foreground and wait for it to settle.

        Raises:
            WindowFocusError: window not connected or set_focus failed.
        """
        if self._window is None:
            raise WindowFocusError("No window connected", {})
        try:
            self._window.set_focus()
            time.sleep(delay)
        except Exception as exc:
            raise WindowFocusError("Failed to focus Discord window", {}) from exc

    def get_focused_element(self) -> Any:
        """Return the UIA element that currently has keyboard focus.

        Returns None on any failure so callers can degrade gracefully.
        Never raises.
        """
        if self._window is None:
            return None
        try:
            return self._window.get_focus()
        except Exception:
            return None

    @property
    def title(self) -> str:
        """Window title text, or empty string if unavailable."""
        if self._window is None:
            return ""
        try:
            return str(self._window.window_text())
        except Exception:
            return ""
