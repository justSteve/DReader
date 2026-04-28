"""Discord scraper using Playwright with AX-tree-first selectors.

Replaces the Selenium-based discord_web_scraper.py. Uses role-based locators
and stable ID-attribute selectors. Never uses obfuscated CSS class names.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from playwright.sync_api import (  # type: ignore[import-untyped]
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from .logger import create_logger


@dataclass
class DiscordMessage:
    """Extracted Discord message."""

    content: str
    author: str | None = None
    timestamp: str | None = None
    message_id: str | None = None
    is_reply: bool = False


def clean_message_id(raw_id: str | None) -> str | None:
    """Extract Discord message ID from DOM element id like 'chat-messages-1234567890'."""
    if not raw_id:
        return None
    parts = raw_id.split("-")
    if len(parts) >= 3:
        return parts[-1]
    return raw_id


def parse_raw_messages(
    raw: list[dict], limit: int = 200
) -> list[DiscordMessage]:
    """Parse raw message dicts (from DOM extraction) into DiscordMessage objects.

    Skips entries with empty content or missing ID.
    """
    messages: list[DiscordMessage] = []
    for entry in raw:
        if len(messages) >= limit:
            break
        content = (entry.get("content") or "").strip()
        raw_id = entry.get("id")
        msg_id = clean_message_id(raw_id)
        if not content or not msg_id:
            continue
        messages.append(
            DiscordMessage(
                content=content,
                author=entry.get("author"),
                timestamp=entry.get("timestamp"),
                message_id=msg_id,
                is_reply=entry.get("reply_id") is not None,
            )
        )
    return messages


# JavaScript executed inside the page to batch-extract message data.
# Uses stable selectors: element IDs and semantic HTML — no CSS classes.
# Adjust if Task 2 probe reveals different DOM structure.
_EXTRACT_JS = """
() => {
    const items = document.querySelectorAll('li[id^="chat-messages-"]');
    return Array.from(items).map(el => {
        const heading = el.querySelector('h3');
        const time = el.querySelector('time');
        const content = el.querySelector('[id^="message-content-"]');
        const reply = el.querySelector('[id^="message-reply-"]');
        return {
            id: el.id || null,
            author: heading ? heading.textContent.trim() : null,
            timestamp: time ? time.getAttribute('datetime') : null,
            content: content ? content.textContent.trim() : null,
            reply_id: reply ? reply.id.replace('message-reply-', '') : null,
        };
    });
}
"""

# Scroll script: scrolls the message container up by one viewport and
# returns whether we're at the top.
_SCROLL_JS = """
() => {
    const scroller = document.querySelector('[class*="scrollerInner"]');
    if (!scroller) return { at_top: true };
    const parent = scroller.parentElement;
    if (!parent) return { at_top: true };
    const before = parent.scrollTop;
    parent.scrollTop = 0;
    return { before, after: parent.scrollTop, at_top: before === parent.scrollTop || parent.scrollTop === 0 };
}
"""


class PlaywrightDiscordScraper:
    """Scrapes Discord messages using Playwright with a persistent browser context."""

    def __init__(
        self,
        user_data_dir: str = "data/playwright-profile",
        headless: bool = False,
    ) -> None:
        self._user_data_dir = str(Path(user_data_dir).resolve())
        self._headless = headless
        self._pw: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._log = create_logger("retrieval.playwright")

    def start(self) -> None:
        """Launch Chrome with a persistent profile. Auth state persists across runs."""
        Path(self._user_data_dir).mkdir(parents=True, exist_ok=True)
        self._pw = sync_playwright().start()
        self._context = self._pw.chromium.launch_persistent_context(
            user_data_dir=self._user_data_dir,
            headless=self._headless,
            viewport={"width": 1280, "height": 720},
            args=["--disable-blink-features=AutomationControlled"],
        )
        self._page = (
            self._context.pages[0] if self._context.pages else self._context.new_page()
        )
        self._log.info("Browser launched", {"profile": self._user_data_dir})

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Browser not started — call start() first")
        return self._page

    def navigate_to_channel(self, server_id: str, channel_id: str) -> None:
        url = f"https://discord.com/channels/{server_id}/{channel_id}"
        self.page.goto(url, wait_until="networkidle")
        self._log.info("Navigated", {"url": url})

    def wait_for_login(self, timeout: int = 300) -> bool:
        """Wait for the chat input to appear, indicating a logged-in session."""
        self._log.info("Waiting for login", {"timeout_s": timeout})
        try:
            self.page.wait_for_selector(
                '[data-slate-editor="true"]', timeout=timeout * 1000
            )
            self._log.info("Login detected")
            return True
        except Exception:
            self._log.error("Login timeout")
            return False

    def extract_messages(self, limit: int = 200) -> list[DiscordMessage]:
        """Extract messages from the current channel using batch DOM evaluation."""
        raw: list[dict[str, Any]] = self.page.evaluate(_EXTRACT_JS)
        self._log.debug("Raw DOM elements", {"count": len(raw)})
        return parse_raw_messages(raw, limit=limit)

    def scroll_up(self) -> bool:
        """Scroll up to load older messages. Returns True if at top."""
        result: dict[str, Any] = self.page.evaluate(_SCROLL_JS)
        at_top = result.get("at_top", True)
        if at_top:
            self._log.info("Reached top of channel")
        self.page.wait_for_timeout(2000)
        return at_top

    def close(self) -> None:
        if self._context:
            self._context.close()
            self._context = None
            self._page = None
            self._log.info("Browser closed")
        if self._pw:
            self._pw.stop()
            self._pw = None
