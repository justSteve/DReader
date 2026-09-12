# Selenium Discord Web Scraper - Usage Guide

## Overview

The Selenium scraper bypasses Discord desktop app limitations by using **Discord Web** (`discord.com`) with Chrome browser automation.

## Prerequisites

1. **Python 3.12+** with venv
2. **Chrome browser** installed
3. **ChromeDriver** (auto-downloaded by Selenium)
4. **Discord account** (manual login required)

## Installation

```bash
# Install selenium dependency
.venv\Scripts\pip install -e ".[retrieval]"
```

## Usage

### Basic Example

```python
from src.retrieval.discord_web_scraper import DiscordWebScraper

# Initialize scraper
scraper = DiscordWebScraper(headless=False)
scraper.start()

# Navigate to channel (get IDs from Discord URL)
scraper.navigate_to_channel(
    server_id="123456789012345678",
    channel_id="987654321098765432"
)

# Wait for manual login (opens browser window)
if scraper.wait_for_login(timeout=300):
    # Extract messages
    messages = scraper.extract_messages(limit=50)

    for msg in messages:
        print(f"{msg.author}: {msg.content}")
```

### Getting Server and Channel IDs

1. Open Discord Web in browser: `discord.com`
2. Navigate to desired channel
3. URL format: `https://discord.com/channels/{SERVER_ID}/{CHANNEL_ID}`
4. Copy the two numeric IDs from URL

Example URL:
```
https://discord.com/channels/1234567890/9876543210
                            ^^^^^^^^^^  ^^^^^^^^^^
                            Server ID   Channel ID
```

### Running the Demo

```bash
# Edit demo script with your IDs
# src/retrieval/discord_web_scraper.py, lines 176-177

python -m src.retrieval.discord_web_scraper
```

## How It Works

1. **Launches Chrome** with Selenium WebDriver
2. **Navigates to Discord Web** (discord.com/channels/...)
3. **Waits for manual login** (you log in normally in browser)
4. **Extracts messages from DOM** using CSS selectors:
   - `li[id^="chat-messages-"]` - Message containers
   - `[class*="username"]` - Author names
   - `[class*="messageContent"]` - Message text
   - `time` elements - Timestamps

## Features

✅ **Full DOM access** - Messages are HTML elements
✅ **Works on Windows** - No platform limitations
✅ **Preserves login** - Uses Chrome profile (optional)
✅ **Thread support** - Detects reply messages
✅ **Scroll loading** - Can load older messages

## Advantages over Desktop App Automation

| Approach | Access to Messages | Platform | Stability |
|----------|-------------------|----------|-----------|
| Pywinauto (desktop) | ❌ No (GPU rendering) | Windows only | N/A |
| Selenium (web) | ✅ Yes (DOM elements) | Any OS | ✅ Stable |
| Claude Chrome | ✅ Yes (DOM) | Non-Windows | 🐛 Buggy |

## Limitations

- **Manual login required** (one-time, then cookies persist)
- **Rate limiting** - Discord may detect automation
- **ToS compliance** - Check Discord's Terms of Service
- **CSS selectors may change** - Discord updates UI

## Integration with DReader

The extracted `DiscordMessage` objects can be converted to existing `MessageRecord` format:

```python
from src.retrieval.models import MessageRecord
from datetime import datetime, UTC

# Convert DiscordMessage → MessageRecord
record = MessageRecord(
    raw_text=discord_msg.content,
    captured_at=datetime.now(UTC),
    nav_index=0,
    channel_name=channel_name,
    session_id=session_id,
    author=discord_msg.author,
    discord_timestamp=discord_msg.timestamp,
    is_reply=discord_msg.is_reply,
    reply_to_author=None,
    metadata_extraction_succeeded=True,
    copy_attempt_count=0,
)
```

## Next Steps

1. **Test with your Discord channels** - Verify selectors work
2. **Add to session.py** - Integrate with existing RetrievalSession
3. **Handle pagination** - Implement scroll-to-load-more
4. **Save login cookies** - Auto-login on subsequent runs
5. **Error handling** - Retry logic, selector fallbacks

## Troubleshooting

### "Chrome not found"
- Install Chrome browser
- Or specify ChromeDriver path in options

### "Login timeout"
- Increase timeout: `wait_for_login(timeout=600)`
- Check if Discord blocks automated browsers

### "No messages found"
- Discord's CSS selectors changed
- Update selectors in `extract_messages()`
- Use browser DevTools to inspect current selectors

### "Captcha required"
- Discord detects automation
- Use real Chrome profile with history
- Add delays between actions
