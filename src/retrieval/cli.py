"""CLI for DReader Playwright scraper."""
from __future__ import annotations

import argparse

from .logger import create_logger
from .registry import ChannelTarget, Registry
from .scrape_session import PlaywrightScrapeSession


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape Discord channel(s) via Playwright"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--target", help="Channel ID, name substring, or server ID to scrape"
    )
    group.add_argument(
        "--all", action="store_true", help="Scrape all channels in registry"
    )
    group.add_argument(
        "--channel-id", help="Direct channel ID (requires --server-id)"
    )
    parser.add_argument("--server-id", help="Direct server ID (with --channel-id)")
    parser.add_argument(
        "--config", default="discord-config.yaml", help="Registry config path"
    )
    parser.add_argument(
        "--db-path", default="data/dreader.db", help="SQLite database path"
    )
    parser.add_argument(
        "--max-scrolls", type=int, default=10, help="Max scroll passes"
    )
    parser.add_argument("--headless", action="store_true", help="Run headless")
    parser.add_argument(
        "--profile-dir",
        default="data/playwright-profile",
        help="Playwright persistent profile dir",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_targets",
        help="List targets and exit",
    )
    args = parser.parse_args()

    if args.channel_id:
        if not args.server_id:
            parser.error("--channel-id requires --server-id")
        targets: list[ChannelTarget] = [
            ChannelTarget(
                channel_id=args.channel_id,
                channel_name=args.channel_id,
                server_id=args.server_id,
                server_name=args.server_id,
            )
        ]
    else:
        registry = Registry.load(args.config)
        if args.list_targets:
            for t in registry.targets:
                print(
                    f"  {t.server_name}/{t.channel_name}  "
                    f"({t.server_id}/{t.channel_id})"
                )
            print(
                f"\n{len(registry.targets)} channels across "
                f"{len(registry.server_ids)} servers"
            )
            return
        targets = (
            registry.targets if args.all else registry.find(args.target or "")
        )
        if not targets:
            print(f"No targets matched '{args.target}'")
            return

    log = create_logger("retrieval.cli")
    log.info("Scrape run starting", {"channels": len(targets)})
    results: list[dict[str, object]] = []

    for t in targets:
        log.info(
            "Scraping channel",
            {"server": t.server_name, "channel": t.channel_name},
        )
        session = PlaywrightScrapeSession(
            server_id=t.server_id,
            channel_id=t.channel_id,
            server_name=t.server_name,
            channel_name=t.channel_name,
            db_path=args.db_path,
            headless=args.headless,
            max_scrolls=args.max_scrolls,
            user_data_dir=args.profile_dir,
        )
        result = session.run()
        results.append(result)
        msgs = result.get("messages_scraped", 0)
        print(f"  {t.channel_name}: {result.get('status')} ({msgs} msgs)")

    total = sum(int(r.get("messages_scraped", 0) or 0) for r in results)
    ok = sum(1 for r in results if r.get("status") == "completed")
    print(f"\nDone: {ok}/{len(results)} channels, {total} messages total")
