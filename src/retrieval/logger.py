"""JSONL structured logger that byte-for-byte matches the TypeScript logger schema.

Log file:   data/logs/dreader-{YYYY-MM-DD}.jsonl
JSONL line: {"timestamp":"...","level":"info","component":"retrieval.session",
             "message":"...","data":{...}}
Console:    12:00:00 INFO  [retrieval.session] ... {...}
"""
from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any

_LEVEL_ORDER: dict[str, int] = {
    "debug": 0,
    "info": 1,
    "warn": 2,
    "error": 3,
}


def _fmt_ts(dt: datetime) -> str:
    """Format datetime as JS-compatible ISO string: 2026-02-18T12:00:00.000Z"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


class ComponentLogger:
    """Structured JSONL logger that mirrors the TypeScript ComponentLogger."""

    def __init__(
        self,
        component: str,
        min_level: str,
        log_dir: str,
        use_console: bool = True,
    ) -> None:
        self._component = component
        self._min_level_name = min_level
        self._min_level = _LEVEL_ORDER.get(min_level, 1)
        self._log_dir = Path(log_dir)
        self._use_console = use_console
        self._log_file: IO[str] | None = None
        self._current_date: str = ""

    def _get_file(self) -> IO[str]:
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        if today != self._current_date or self._log_file is None:
            if self._log_file is not None:
                self._log_file.close()
            self._current_date = today
            self._log_dir.mkdir(parents=True, exist_ok=True)
            log_path = self._log_dir / f"dreader-{today}.jsonl"
            self._log_file = open(log_path, "a", encoding="utf-8")
        return self._log_file

    def _log(self, level: str, message: str, data: dict[str, Any] | None = None) -> None:
        if _LEVEL_ORDER.get(level, 0) < self._min_level:
            return
        now = datetime.now(UTC)
        entry: dict[str, Any] = {
            "timestamp": _fmt_ts(now),
            "level": level,
            "component": self._component,
            "message": message,
        }
        if data is not None:
            entry["data"] = data
        line = json.dumps(entry) + "\n"
        f = self._get_file()
        f.write(line)
        f.flush()
        if self._use_console:
            time_part = _fmt_ts(now)[11:19]
            lvl_part = level.upper().ljust(5)
            ctx = f" {json.dumps(data)}" if data else ""
            sys.stderr.write(f"{time_part} {lvl_part} [{self._component}] {message}{ctx}\n")

    def debug(self, message: str, data: dict[str, Any] | None = None) -> None:
        self._log("debug", message, data)

    def info(self, message: str, data: dict[str, Any] | None = None) -> None:
        self._log("info", message, data)

    def warn(self, message: str, data: dict[str, Any] | None = None) -> None:
        self._log("warn", message, data)

    def error(self, message: str, data: dict[str, Any] | None = None) -> None:
        self._log("error", message, data)

    def child(self, sub: str) -> ComponentLogger:
        """Return a child logger with component name extended by sub."""
        return ComponentLogger(
            f"{self._component}.{sub}",
            self._min_level_name,
            str(self._log_dir),
            self._use_console,
        )

    def close(self) -> None:
        if self._log_file is not None:
            self._log_file.close()
            self._log_file = None


def create_logger(
    component: str,
    log_level: str = "info",
    log_dir: str = "data/logs",
    use_console: bool = True,
) -> ComponentLogger:
    """Factory function matching the TypeScript createLogger convention."""
    level = os.environ.get("LOG_LEVEL", log_level)
    return ComponentLogger(component, level, log_dir, use_console)
