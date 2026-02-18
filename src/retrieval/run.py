"""CLI entry point for the DReader retrieval subsystem.

Usage (Windows, via bat launcher):
    python.exe src\\retrieval\\run.py --channel general --count 50

Usage (from WSL2):
    cmd.exe /c scripts\\run_retrieval.bat --channel general --count 50
"""
from __future__ import annotations

import argparse
import sys

from .config import RetrievalConfig
from .errors import SessionError
from .session import RetrievalSession


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DReader: retrieve Discord messages via keyboard automation",
    )
    parser.add_argument("--channel", required=True, help="Discord channel name")
    parser.add_argument(
        "--count", type=int, required=True, help="Number of messages to retrieve"
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warn", "error"],
        dest="log_level",
        help="Minimum log level (default: info)",
    )
    args = parser.parse_args()

    config = RetrievalConfig(
        channel_name=args.channel,
        message_count=args.count,
        log_level=args.log_level,
    )

    try:
        session = RetrievalSession(config)
        result = session.execute()
    except SessionError as exc:
        sys.stderr.write(f"Fatal error: {exc}\n")
        return 1

    sys.stderr.write(
        f"Retrieved {len(result.records)} messages from #{config.channel_name}\n"
    )
    if result.errors:
        sys.stderr.write(f"  {len(result.errors)} messages failed to capture\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
