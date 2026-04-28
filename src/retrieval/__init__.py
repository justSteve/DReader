"""DReader retrieval subsystem — Playwright-based Discord scraper."""
from __future__ import annotations

from .db import ScrapeDB
from .discord_playwright_scraper import (
    DiscordMessage,
    PlaywrightDiscordScraper,
    clean_message_id,
    parse_raw_messages,
)
from .errors import DReaderError
from .logger import create_logger
from .registry import ChannelTarget, Registry
from .scrape_session import PlaywrightScrapeSession

__all__ = [
    "ChannelTarget",
    "DiscordMessage",
    "DReaderError",
    "PlaywrightDiscordScraper",
    "PlaywrightScrapeSession",
    "Registry",
    "ScrapeDB",
    "clean_message_id",
    "create_logger",
    "parse_raw_messages",
]
