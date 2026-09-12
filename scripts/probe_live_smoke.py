"""Live smoke probe for dr-2tp: launch persistent-profile browser against Discord Web.

Stage 1: land on discord.com, report login state, screenshot for vision review.
Stage 2 (--channel SERVER_ID CHANNEL_ID): navigate to a channel, screenshot,
and batch-extract messages via the DOM extractor for comparison against vision.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.retrieval.discord_playwright_scraper import PlaywrightDiscordScraper

SHOT_DIR = Path(__file__).resolve().parents[1] / "data" / "probe-shots"
SHOT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    s = PlaywrightDiscordScraper(user_data_dir="data/chrome-profile", headless=False)
    s.start()
    page = s.page
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--login-wait":
            page.goto(
                "https://discord.com/channels/@me",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            wait_s = int(sys.argv[2]) if len(sys.argv) >= 3 else 600
            print(f"Browser open — waiting up to {wait_s}s for interactive login...")
            logged_in = s.wait_for_login(timeout=wait_s)
            print("logged_in:", logged_in)
            if logged_in:
                page.wait_for_timeout(5000)
                shot = SHOT_DIR / "01b-logged-in.png"
                page.screenshot(path=str(shot))
                print("screenshot:", shot)
        elif len(sys.argv) >= 4 and sys.argv[1] == "--channel":
            server_id, channel_id = sys.argv[2], sys.argv[3]
            s.navigate_to_channel(server_id, channel_id)
            logged_in = s.wait_for_login(timeout=30)
            print("logged_in:", logged_in)
            page.wait_for_timeout(5000)
            shot = SHOT_DIR / f"02-channel-{channel_id}.png"
            page.screenshot(path=str(shot))
            print("screenshot:", shot)
            msgs = s.extract_messages(limit=50)
            out = SHOT_DIR / f"02-channel-{channel_id}.json"
            out.write_text(
                json.dumps([m.__dict__ for m in msgs], indent=2, ensure_ascii=False)
            )
            print(f"extracted {len(msgs)} messages -> {out}")
        else:
            page.goto(
                "https://discord.com/channels/@me",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            page.wait_for_timeout(10000)  # let the SPA settle
            print("URL:", page.url)
            print("TITLE:", page.title())
            print("slate-editor count:", page.locator('[data-slate-editor="true"]').count())
            print("login form count:", page.locator('input[name="email"]').count())
            shot = SHOT_DIR / "01-landing.png"
            page.screenshot(path=str(shot))
            print("screenshot:", shot)
    finally:
        s.close()


if __name__ == "__main__":
    main()
