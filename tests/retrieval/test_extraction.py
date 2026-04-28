"""Tests for message extraction logic."""
from __future__ import annotations

from src.retrieval.discord_playwright_scraper import (
    DiscordMessage,
    clean_message_id,
    parse_raw_messages,
)


class TestCleanMessageId:
    def test_standard_format(self) -> None:
        assert clean_message_id("chat-messages-1234567890") == "1234567890"

    def test_none_input(self) -> None:
        assert clean_message_id(None) is None

    def test_empty_string(self) -> None:
        assert clean_message_id("") is None

    def test_short_format(self) -> None:
        assert clean_message_id("1234567890") == "1234567890"

    def test_two_parts(self) -> None:
        assert clean_message_id("chat-1234567890") == "chat-1234567890"


class TestParseRawMessages:
    def test_parses_complete_message(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages)
        assert len(result) == 3  # 4th message has no content, should be skipped

    def test_extracts_fields(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages)
        msg = result[0]
        assert msg.message_id == "1234567890"
        assert msg.author == "Alice"
        assert msg.timestamp == "2026-04-28T12:00:00.000Z"
        assert msg.content == "Hello everyone!"
        assert msg.is_reply is False

    def test_handles_missing_author(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages)
        msg = result[1]
        assert msg.author is None
        assert msg.content == "This is a continuation message (no author header)"

    def test_detects_reply(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages)
        msg = result[2]
        assert msg.is_reply is True
        assert msg.author == "Bob"

    def test_skips_empty_content(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages)
        ids = [m.message_id for m in result]
        assert None not in ids

    def test_respects_limit(self, raw_messages: list[dict]) -> None:
        result = parse_raw_messages(raw_messages, limit=1)
        assert len(result) == 1

    def test_empty_input(self) -> None:
        assert parse_raw_messages([]) == []


# Silence "unused import" — DiscordMessage imported as part of the module
# contract under test.
_ = DiscordMessage
