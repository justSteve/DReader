"""Discord scraper using Playwright with AX-tree-first selectors.

Replaces the Selenium-based discord_web_scraper.py. Uses role-based locators
and stable ID-attribute selectors. Never uses obfuscated CSS class names.
"""
from __future__ import annotations

from dataclasses import dataclass


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
