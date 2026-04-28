"""Shared fixtures for retrieval tests.

RAW_MESSAGES simulates the output of the batch DOM extraction (page.evaluate)
that the scraper runs against Discord's message list. Adjust field values if
the Task 2 probe reveals different DOM structure.
"""
from __future__ import annotations

import pytest


@pytest.fixture()
def raw_messages() -> list[dict]:
    """Sample raw message dicts as returned by the in-page extraction script."""
    return [
        {
            "id": "chat-messages-1234567890",
            "author": "Alice",
            "timestamp": "2026-04-28T12:00:00.000Z",
            "content": "Hello everyone!",
            "reply_id": None,
        },
        {
            "id": "chat-messages-1234567891",
            "author": None,
            "timestamp": "2026-04-28T12:01:00.000Z",
            "content": "This is a continuation message (no author header)",
            "reply_id": None,
        },
        {
            "id": "chat-messages-1234567892",
            "author": "Bob",
            "timestamp": "2026-04-28T12:02:00.000Z",
            "content": "Replying to Alice",
            "reply_id": "1234567890",
        },
        {
            "id": None,
            "author": None,
            "timestamp": None,
            "content": "",
            "reply_id": None,
        },
    ]
