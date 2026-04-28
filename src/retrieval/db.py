"""SQLite access layer for the Selenium scraper.

Writes to the same schema as the TypeScript DatabaseService so both
engines produce interchangeable data.
"""
from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.") + "000Z"


class ScrapeDB:
    """Thin wrapper around the shared DReader SQLite database."""

    def __init__(self, db_path: str = "data/dreader.db") -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._path))
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        schema_path = Path(__file__).resolve().parent.parent / "services" / "schema.sql"
        if schema_path.exists():
            self._conn.executescript(schema_path.read_text())

    def ensure_server(self, server_id: str, name: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO servers (id, name, scraped_at) VALUES (?, ?, ?)",
            (server_id, name, _now_iso()),
        )
        self._conn.commit()

    def ensure_channel(self, channel_id: str, server_id: str, name: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO channels (id, server_id, name) VALUES (?, ?, ?)",
            (channel_id, server_id, name),
        )
        self._conn.commit()

    def create_scrape_job(self, channel_id: str, scrape_type: str = "full") -> int:
        cur = self._conn.execute(
            "INSERT INTO scrape_jobs (channel_id, status, scrape_type, started_at) VALUES (?, ?, ?, ?)",
            (channel_id, "running", scrape_type, _now_iso()),
        )
        self._conn.commit()
        return cur.lastrowid or 0

    def update_job_status(
        self, job_id: int, status: str, error_message: str | None = None
    ) -> None:
        if status in ("completed", "failed"):
            self._conn.execute(
                "UPDATE scrape_jobs SET status = ?, completed_at = ?, error_message = ? WHERE id = ?",
                (status, _now_iso(), error_message, job_id),
            )
        else:
            self._conn.execute(
                "UPDATE scrape_jobs SET status = ?, error_message = ? WHERE id = ?",
                (status, error_message, job_id),
            )
        self._conn.commit()

    def increment_messages_scraped(self, job_id: int, count: int) -> None:
        self._conn.execute(
            "UPDATE scrape_jobs SET messages_scraped = messages_scraped + ? WHERE id = ?",
            (count, job_id),
        )
        self._conn.commit()

    def insert_message(
        self,
        *,
        message_id: str,
        channel_id: str,
        author_id: str,
        author_name: str,
        content: str,
        timestamp: str,
        server_id: str,
        author_avatar_url: str = "",
        reply_to_message_id: str | None = None,
        edited_timestamp: str | None = None,
        is_pinned: bool = False,
        attachment_urls: str = "[]",
        embed_data: str = "[]",
        has_attachments: bool = False,
        has_embeds: bool = False,
    ) -> bool:
        """Insert a message. Returns True if inserted, False if duplicate."""
        message_url = f"https://discord.com/channels/{server_id}/{channel_id}/{message_id}"
        try:
            self._conn.execute(
                """INSERT OR IGNORE INTO messages
                   (id, channel_id, author_id, author_name, author_avatar_url,
                    content, timestamp, reply_to_message_id, edited_timestamp,
                    is_pinned, attachment_urls, embed_data, message_url,
                    has_attachments, has_embeds)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    message_id, channel_id, author_id, author_name, author_avatar_url,
                    content, timestamp, reply_to_message_id, edited_timestamp,
                    1 if is_pinned else 0, attachment_urls, embed_data, message_url,
                    1 if has_attachments else 0, 1 if has_embeds else 0,
                ),
            )
            self._conn.commit()
            return self._conn.total_changes > 0
        except sqlite3.IntegrityError:
            return False

    def close(self) -> None:
        self._conn.close()
