"""Tests for PlaywrightScrapeSession orchestration logic."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.retrieval.discord_playwright_scraper import DiscordMessage
from src.retrieval.scrape_session import PlaywrightScrapeSession


@pytest.fixture()
def mock_scraper() -> MagicMock:
    scraper = MagicMock()
    scraper.wait_for_login.return_value = True
    scraper.extract_messages.return_value = [
        DiscordMessage(
            content="hello",
            author="Alice",
            timestamp="2026-04-28T12:00:00Z",
            message_id="111",
        ),
        DiscordMessage(
            content="world",
            author="Bob",
            timestamp="2026-04-28T12:01:00Z",
            message_id="222",
        ),
    ]
    scraper.scroll_up.return_value = True  # at top after first scroll
    return scraper


@pytest.fixture()
def mock_db() -> MagicMock:
    db = MagicMock()
    db.create_scrape_job.return_value = 1
    db.insert_message.return_value = True
    return db


class TestPlaywrightScrapeSession:
    @patch("src.retrieval.scrape_session.PlaywrightDiscordScraper")
    @patch("src.retrieval.scrape_session.ScrapeDB")
    def test_successful_scrape(
        self,
        mock_db_cls: MagicMock,
        mock_scraper_cls: MagicMock,
        mock_scraper: MagicMock,
        mock_db: MagicMock,
    ) -> None:
        mock_scraper_cls.return_value = mock_scraper
        mock_db_cls.return_value = mock_db

        session = PlaywrightScrapeSession(
            server_id="srv1",
            channel_id="ch1",
            server_name="TestServer",
            channel_name="general",
        )
        result = session.run()

        assert result["status"] == "completed"
        assert result["messages_scraped"] == 2
        mock_db.ensure_server.assert_called_once_with("srv1", "TestServer")
        mock_db.ensure_channel.assert_called_once_with("ch1", "srv1", "general")
        mock_scraper.start.assert_called_once()
        mock_scraper.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch("src.retrieval.scrape_session.PlaywrightDiscordScraper")
    @patch("src.retrieval.scrape_session.ScrapeDB")
    def test_login_timeout(
        self,
        mock_db_cls: MagicMock,
        mock_scraper_cls: MagicMock,
        mock_scraper: MagicMock,
        mock_db: MagicMock,
    ) -> None:
        mock_scraper.wait_for_login.return_value = False
        mock_scraper_cls.return_value = mock_scraper
        mock_db_cls.return_value = mock_db

        session = PlaywrightScrapeSession(
            server_id="srv1",
            channel_id="ch1",
        )
        result = session.run()

        assert result["status"] == "failed"
        assert result["error"] == "login_timeout"
        mock_db.update_job_status.assert_called_with(1, "failed", "Login timeout")

    @patch("src.retrieval.scrape_session.PlaywrightDiscordScraper")
    @patch("src.retrieval.scrape_session.ScrapeDB")
    def test_deduplicates_messages(
        self,
        mock_db_cls: MagicMock,
        mock_scraper_cls: MagicMock,
        mock_db: MagicMock,
    ) -> None:
        scraper = MagicMock()
        scraper.wait_for_login.return_value = True
        # Same messages returned on both passes
        scraper.extract_messages.return_value = [
            DiscordMessage(content="hello", message_id="111"),
        ]
        scraper.scroll_up.side_effect = [False, True]  # not at top, then at top
        mock_scraper_cls.return_value = scraper
        mock_db_cls.return_value = mock_db

        session = PlaywrightScrapeSession(
            server_id="srv1",
            channel_id="ch1",
            max_scrolls=2,
        )
        result = session.run()

        # insert_message called only once despite two extraction passes
        assert mock_db.insert_message.call_count == 1
        assert result["status"] == "completed"
