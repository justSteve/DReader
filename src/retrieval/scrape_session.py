"""Scrape session orchestrator — browser + database."""
from __future__ import annotations

from .db import ScrapeDB
from .discord_playwright_scraper import PlaywrightDiscordScraper
from .logger import create_logger


class PlaywrightScrapeSession:
    """End-to-end scrape: launch browser, extract messages, persist to DB."""

    def __init__(
        self,
        server_id: str,
        channel_id: str,
        server_name: str = "",
        channel_name: str = "",
        db_path: str = "data/dreader.db",
        headless: bool = False,
        max_scrolls: int = 10,
        user_data_dir: str = "data/playwright-profile",
    ) -> None:
        self.server_id = server_id
        self.channel_id = channel_id
        self.server_name = server_name or server_id
        self.channel_name = channel_name or channel_id
        self.max_scrolls = max_scrolls
        self._log = create_logger("retrieval.session")
        self._scraper = PlaywrightDiscordScraper(
            user_data_dir=user_data_dir,
            headless=headless,
        )
        self._db = ScrapeDB(db_path)

    def run(self) -> dict[str, object]:
        """Execute the full scrape. Returns summary dict."""
        self._db.ensure_server(self.server_id, self.server_name)
        self._db.ensure_channel(self.channel_id, self.server_id, self.channel_name)
        job_id = self._db.create_scrape_job(self.channel_id)
        self._log.info("Scrape job created", {"job_id": job_id})

        total_inserted = 0
        seen_ids: set[str] = set()

        try:
            self._scraper.start()
            self._scraper.navigate_to_channel(self.server_id, self.channel_id)

            if not self._scraper.wait_for_login(timeout=300):
                self._db.update_job_status(job_id, "failed", "Login timeout")
                return {"job_id": job_id, "status": "failed", "error": "login_timeout"}

            for scroll_num in range(self.max_scrolls + 1):
                messages = self._scraper.extract_messages()
                new_count = 0
                for msg in messages:
                    if not msg.message_id or msg.message_id in seen_ids:
                        continue
                    seen_ids.add(msg.message_id)
                    self._db.insert_message(
                        message_id=msg.message_id,
                        channel_id=self.channel_id,
                        author_id=msg.author or "unknown",
                        author_name=msg.author or "unknown",
                        content=msg.content,
                        timestamp=msg.timestamp or "",
                        server_id=self.server_id,
                        reply_to_message_id=None,
                    )
                    new_count += 1

                total_inserted += new_count
                if new_count > 0:
                    self._db.increment_messages_scraped(job_id, new_count)
                self._log.info(
                    "Scroll pass",
                    {"scroll": scroll_num, "new": new_count, "total": total_inserted},
                )

                if scroll_num < self.max_scrolls:
                    at_top = self._scraper.scroll_up()
                    if at_top:
                        break

            self._db.update_job_status(job_id, "completed")
            self._log.info(
                "Scrape complete",
                {"job_id": job_id, "messages": total_inserted},
            )
            return {
                "job_id": job_id,
                "status": "completed",
                "messages_scraped": total_inserted,
            }

        except Exception as e:
            self._db.update_job_status(job_id, "failed", str(e))
            self._log.error("Scrape failed", {"job_id": job_id, "error": str(e)})
            return {"job_id": job_id, "status": "failed", "error": str(e)}
        finally:
            self._scraper.close()
            self._db.close()
