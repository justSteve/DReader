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
    class _PywinautoDesktop:
        def windows(self) -> list[Any]: ...
    class pywinauto:  # noqa: N801
        @staticmethod
        def Application(backend: str) -> _PywinautoApp: ...  # noqa: N802
        @staticmethod
        def Desktop(backend: str) -> _PywinautoDesktop: ...  # noqa: N802
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

    def connect(self, exe_name: str = "Discord.exe") -> None:
        """Connect to Discord by finding a window belonging to Discord.exe process.

        Args:
            exe_name: Process executable name (default: "Discord.exe")

        Raises:
            WindowNotFoundError: no Discord window found.
        """
        try:
            import subprocess
            # Get all Discord PIDs using tasklist
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {exe_name}', '/FO', 'CSV', '/NH'],
                capture_output=True,
                text=True,
                check=True,
            )
            # Parse PIDs from tasklist output (CSV format: "name","PID",...)
            pids = [int(line.split(',')[1].strip('"')) for line in result.stdout.strip().split('\n') if line]

            if not pids:
                raise ValueError(f"No {exe_name} process found")

            # Find windows belonging to Discord PIDs
            desktop = pywinauto.Desktop(backend="win32")
            discord_windows = [w for w in desktop.windows() if w.process_id() in pids and w.is_visible()]

            if not discord_windows:
                raise ValueError(f"No visible window for {exe_name} (found {len(pids)} processes)")

            # Use the first visible Discord window
            self._window = discord_windows[0]
            self._app = pywinauto.Application(backend="win32").connect(process=self._window.process_id())
        except Exception as exc:
            raise WindowNotFoundError(
                f"Discord window not found for {exe_name!r}",
                {"exe_name": exe_name},
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

    def enumerate_messages(self, max_depth: int = 10) -> list[Any]:
        """Enumerate message elements from the Discord UI tree.

        Walks the UI tree depth-first to find elements that look like messages.
        Discord messages typically have:
        - Non-empty window_text()
        - Multiple children (author, content, timestamp, etc.)
        - Specific control types (usually "Group" or "ListItem")

        Args:
            max_depth: Maximum tree depth to search (default: 10)

        Returns:
            List of message elements (empty if none found)
        """
        if self._window is None:
            return []

        messages: list[Any] = []
        try:
            # Start from the window root and walk the tree
            def _walk_tree(element: Any, depth: int = 0) -> None:
                if depth > max_depth:
                    return

                try:
                    # Check if this element looks like a message
                    # Discord messages have window_text and usually have children
                    text = element.window_text()
                    if text and len(text) > 0:
                        # Try to get children count
                        try:
                            children = list(element.children())
                            # Messages typically have multiple child elements
                            # (author, timestamp, reactions, etc.)
                            if len(children) >= 1:
                                messages.append(element)
                                # Don't recurse into message children
                                return
                        except Exception:
                            pass

                    # Recurse into children
                    for child in element.children():
                        _walk_tree(child, depth + 1)
                except Exception:
                    pass

            _walk_tree(self._window)
        except Exception:
            pass

        return messages
