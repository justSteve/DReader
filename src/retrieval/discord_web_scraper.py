"""Discord Web scraper using Selenium - proof of concept.

This approach uses Discord Web (discord.com) instead of the desktop app,
bypassing the Chromium rendering limitation that blocks pywinauto.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from selenium import webdriver  # type: ignore[import-untyped]
from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore[import-untyped]
from selenium.webdriver.common.by import By  # type: ignore[import-untyped]
from selenium.webdriver.support import expected_conditions as EC  # type: ignore[import-untyped]
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore[import-untyped]
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # type: ignore[import-untyped]


@dataclass
class DiscordMessage:
    """Extracted Discord message."""

    content: str
    author: str | None = None
    timestamp: str | None = None
    message_id: str | None = None
    is_reply: bool = False


class DiscordWebScraper:
    """Scrapes Discord messages using Selenium + Discord Web."""

    def __init__(self, headless: bool = False):
        """Initialize scraper.

        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver: WebDriver | None = None

    def start(self) -> None:
        """Start Chrome browser."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        # Keep browser open after script ends (for manual login)
        options.add_experimental_option("detach", True)
        # Use existing Chrome profile to preserve login session
        # options.add_argument(r"user-data-dir=C:\Users\steve\AppData\Local\Google\Chrome\User Data")

        self.driver = webdriver.Chrome(options=options)

    def navigate_to_channel(self, server_id: str, channel_id: str) -> None:
        """Navigate to a Discord channel.

        Args:
            server_id: Discord server/guild ID
            channel_id: Discord channel ID
        """
        if not self.driver:
            raise RuntimeError("Driver not started - call start() first")

        url = f"https://discord.com/channels/{server_id}/{channel_id}"
        self.driver.get(url)

        # Wait for page to load
        time.sleep(3)

    def wait_for_login(self, timeout: int = 300) -> bool:
        """Wait for user to log in manually.

        Args:
            timeout: Max seconds to wait for login

        Returns:
            True if logged in, False if timeout
        """
        if not self.driver:
            return False

        print("Please log in to Discord in the browser window...")
        print(f"Waiting up to {timeout} seconds...")

        try:
            # Wait for the chat input box to appear (indicates logged in)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-slate-editor="true"]'))
            )
            print("Login detected!")
            return True
        except TimeoutException:
            print("Login timeout")
            return False

    def extract_messages(self, limit: int = 50) -> list[DiscordMessage]:
        """Extract messages from the current channel.

        Args:
            limit: Maximum number of messages to extract

        Returns:
            List of DiscordMessage objects
        """
        if not self.driver:
            raise RuntimeError("Driver not started")

        messages: list[DiscordMessage] = []

        try:
            # Discord message container selector
            # Messages are in <li> elements with data-list-item-id attribute
            message_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                'li[id^="chat-messages-"]'
            )

            print(f"Found {len(message_elements)} message elements")

            for elem in message_elements[:limit]:
                try:
                    # Extract message ID
                    msg_id = elem.get_attribute('id')

                    # Extract author - usually in a span or h3 with specific classes
                    author = None
                    try:
                        author_elem = elem.find_element(By.CSS_SELECTOR, '[class*="username"]')
                        author = author_elem.text
                    except NoSuchElementException:
                        pass

                    # Extract timestamp
                    timestamp = None
                    try:
                        time_elem = elem.find_element(By.CSS_SELECTOR, 'time')
                        timestamp = time_elem.get_attribute('datetime')
                    except NoSuchElementException:
                        pass

                    # Extract message content
                    content = ""
                    try:
                        # Message content is usually in a div with specific class
                        content_elem = elem.find_element(By.CSS_SELECTOR, '[class*="messageContent"]')
                        content = content_elem.text
                    except NoSuchElementException:
                        # Fallback: get all text
                        content = elem.text

                    # Check if it's a reply
                    is_reply = False
                    try:
                        elem.find_element(By.CSS_SELECTOR, '[class*="repliedMessage"]')
                        is_reply = True
                    except NoSuchElementException:
                        pass

                    if content:  # Only add if we got content
                        messages.append(DiscordMessage(
                            content=content,
                            author=author,
                            timestamp=timestamp,
                            message_id=msg_id,
                            is_reply=is_reply,
                        ))

                except Exception as e:
                    print(f"Error extracting message: {e}")
                    continue

        except Exception as e:
            print(f"Error finding messages: {e}")

        return messages

    def scroll_to_load_more(self, scroll_count: int = 3) -> None:
        """Scroll up to load older messages.

        Args:
            scroll_count: Number of times to scroll
        """
        if not self.driver:
            return

        for _ in range(scroll_count):
            # Scroll to top of message container
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)  # Wait for messages to load

    def close(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None


def main() -> None:
    """Demo: scrape messages from a Discord channel."""
    # Example usage - replace with actual IDs
    SERVER_ID = "YOUR_SERVER_ID"
    CHANNEL_ID = "YOUR_CHANNEL_ID"

    scraper = DiscordWebScraper(headless=False)
    scraper.start()

    print("Opening Discord...")
    scraper.navigate_to_channel(SERVER_ID, CHANNEL_ID)

    # Wait for manual login
    if not scraper.wait_for_login(timeout=300):
        print("Failed to detect login")
        scraper.close()
        return

    print("\nExtracting messages...")
    messages = scraper.extract_messages(limit=10)

    print(f"\n=== Extracted {len(messages)} messages ===\n")
    for i, msg in enumerate(messages, 1):
        print(f"[{i}] {msg.author} ({msg.timestamp}):")
        print(f"    {msg.content[:100]}...")
        print(f"    ID: {msg.message_id}, Reply: {msg.is_reply}\n")

    # Don't close - keep browser open for inspection
    # scraper.close()


if __name__ == "__main__":
    main()
