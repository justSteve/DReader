"""Vision driver for dr-s8g: long-lived Playwright browser exposing a tiny HTTP
command API so a model can run a computer-use loop (screenshot -> decide -> act).

Commands (POST JSON to http://127.0.0.1:8765/):
  {"op":"goto","url":...}
  {"op":"shot","name":...}            -> {"path":...}
  {"op":"click","x":..,"y":..}
  {"op":"move","x":..,"y":..}
  {"op":"scroll","x":..,"y":..,"dy":..}   (mouse wheel at position)
  {"op":"type","text":...}
  {"op":"key","key":...}              (e.g. "PageUp", "Escape")
  {"op":"eval","js":...}              (ground-truth only)
  {"op":"url"}
  {"op":"quit"}
"""
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.retrieval.discord_playwright_scraper import PlaywrightDiscordScraper

SHOT_DIR = Path(__file__).resolve().parents[1] / "data" / "vision-shots"
SHOT_DIR.mkdir(parents=True, exist_ok=True)

import os
import urllib.request

from playwright.sync_api import sync_playwright

CDP = os.environ.get("VISION_CDP")  # e.g. http://172.25.112.1:9223 (Windows Chrome via bridge)
scraper = PlaywrightDiscordScraper(user_data_dir="data/chrome-profile", headless=False)
if CDP:
    # Chrome advertises ws://localhost:9222/...; rewrite host to the bridge so WSL can reach it.
    ver = json.loads(urllib.request.urlopen(CDP + "/json/version", timeout=10).read())
    ws = re.sub(r"^ws://[^/]+", "ws://" + CDP.split("//", 1)[1], ver["webSocketDebuggerUrl"])
    scraper._pw = sync_playwright().start()
    browser = scraper._pw.chromium.connect_over_cdp(ws)
    ctx = browser.contexts[0]
    pages = [pg for pg in ctx.pages if "discord.com" in pg.url] or ctx.pages
    page = pages[0] if pages else ctx.new_page()
    page.bring_to_front()
    scraper._context = ctx
    scraper._page = page
    print("attached over CDP:", ws, "->", page.url, flush=True)
else:
    scraper.start()
    page = scraper.page
counter = {"n": 0}


def handle(cmd: dict) -> dict:
    op = cmd.get("op")
    if op == "goto":
        page.goto(cmd["url"], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(cmd.get("settle_ms", 4000))
        return {"url": page.url}
    if op == "shot":
        counter["n"] += 1
        name = cmd.get("name") or f"{counter['n']:03d}"
        p = SHOT_DIR / f"{name}.png"
        page.screenshot(path=str(p))
        return {"path": str(p), "url": page.url}
    if op == "click":
        page.mouse.click(cmd["x"], cmd["y"], button=cmd.get("button", "left"))
        page.wait_for_timeout(cmd.get("settle_ms", 1500))
        return {"ok": True}
    if op == "move":
        page.mouse.move(cmd["x"], cmd["y"])
        return {"ok": True}
    if op == "scroll":
        page.mouse.move(cmd.get("x", 640), cmd.get("y", 400))
        page.mouse.wheel(0, cmd["dy"])
        page.wait_for_timeout(cmd.get("settle_ms", 1500))
        return {"ok": True}
    if op == "type":
        page.keyboard.type(cmd["text"], delay=30)
        return {"ok": True}
    if op == "key":
        page.keyboard.press(cmd["key"])
        page.wait_for_timeout(cmd.get("settle_ms", 800))
        return {"ok": True}
    if op == "eval":
        return {"result": page.evaluate(cmd["js"])}
    if op == "extract":
        msgs = scraper.extract_messages(limit=cmd.get("limit", 200))
        return {"messages": [m.__dict__ for m in msgs]}
    if op == "url":
        return {"url": page.url}
    if op == "quit":
        raise SystemExit
    return {"error": f"unknown op {op}"}


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        cmd = json.loads(self.rfile.read(n) or b"{}")
        try:
            out = handle(cmd)
        except SystemExit:
            self._send({"bye": True})
            if not CDP:
                scraper.close()
            raise
        except Exception as e:  # noqa: BLE001
            out = {"error": repr(e)}
        self._send(out)

    def _send(self, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


print("vision driver listening on 127.0.0.1:8765", flush=True)
try:
    HTTPServer(("127.0.0.1", 8765), H).serve_forever()
except SystemExit:
    pass
