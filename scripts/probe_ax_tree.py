"""One-shot probe of Discord's accessibility tree.

Usage:
    python scripts/probe_ax_tree.py

Launches a persistent-context browser. You log in to Discord manually,
navigate to any channel with messages, then press Enter in the terminal.
The script captures the AX tree and prints the message-list structure.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


def find_node(tree: dict, role: str, name_re: str = "") -> dict | None:
    """DFS search for an AX node by role and optional name regex."""
    if tree.get("role") == role:
        if not name_re or re.search(name_re, tree.get("name", ""), re.IGNORECASE):
            return tree
    for child in tree.get("children", []):
        hit = find_node(child, role, name_re)
        if hit:
            return hit
    return None


def main() -> None:
    profile_dir = str(Path("data/playwright-profile").resolve())
    Path(profile_dir).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            viewport={"width": 1280, "height": 720},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://discord.com/channels/@me")

        input(
            "\n>>> Log in to Discord, navigate to a channel with messages,\n"
            ">>> then press Enter here to capture the AX tree...\n"
        )

        snapshot = page.accessibility.snapshot()
        if not snapshot:
            print("ERROR: accessibility.snapshot() returned None")
            ctx.close()
            return

        out_path = Path("data/ax-tree-snapshot.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(snapshot, indent=2))
        print(f"\nFull AX tree saved to {out_path}")

        msg_list = find_node(snapshot, "list", "Messages in")
        if not msg_list:
            print("WARNING: Could not find list node matching 'Messages in'")
            print("Roles at top level:", [c.get("role") for c in snapshot.get("children", [])])
        else:
            children = msg_list.get("children", [])
            listitems = [c for c in children if c.get("role") == "listitem"]
            print(f"\nMessage list: name='{msg_list.get('name', '')}', {len(listitems)} listitems")

            if listitems:
                print("\n--- First message listitem (full subtree) ---")
                print(json.dumps(listitems[0], indent=2))
                print("\n--- Second message listitem ---")
                if len(listitems) > 1:
                    print(json.dumps(listitems[1], indent=2))

        # Also capture DOM-level info for the first few messages
        dom_info = page.evaluate("""
            () => {
                const items = document.querySelectorAll('li[id^="chat-messages-"]');
                return Array.from(items).slice(0, 3).map(el => ({
                    id: el.id,
                    hasHeading: !!el.querySelector('h3'),
                    hasTime: !!el.querySelector('time'),
                    hasContentById: !!el.querySelector('[id^="message-content-"]'),
                    hasReplyById: !!el.querySelector('[id^="message-reply-"]'),
                    headingText: el.querySelector('h3')?.textContent?.trim() || null,
                    timeAttr: el.querySelector('time')?.getAttribute('datetime') || null,
                    contentText: (el.querySelector('[id^="message-content-"]')
                        ?.textContent?.trim()?.slice(0, 80)) || null,
                }));
            }
        """)
        print("\n--- DOM-level selector validation (first 3 messages) ---")
        for info in dom_info:
            print(json.dumps(info, indent=2))

        ctx.close()


if __name__ == "__main__":
    main()
