# Vision-Driven Discord Scrape — Experiment Report (dr-s8g)

**Date:** 2026-08-15
**Question:** Can a Fable 5-grade model scrape a Discord channel using only
computer control — screenshots in, mouse/keyboard out — with no DOM access
for navigation or reading?
**Answer:** Yes. Navigation and transcription both worked; text fidelity was
character-exact on 6/7 messages, and on the 7th the vision read was correct
where the existing DOM extractor was wrong.

## Setup

| Piece | Where | Role |
|---|---|---|
| `tools/chrome-bridge.py` | runs on **Windows** | Raw TCP relay `0.0.0.0:9223 → [::1]:9222`, exposes the logged-in Windows Chrome's DevTools to WSL |
| `scripts/vision_driver.py` | runs in **WSL** (tmux) | Long-lived Playwright process attached over CDP; tiny HTTP API on `127.0.0.1:8765` — `shot`, `click`, `scroll`, `type`, `key`, `goto`, `eval`, `extract` |
| The model | Claude Code session | Computer-use loop: `shot` → look → decide → `click`/`scroll` → repeat |

Launch (WSL): `VISION_CDP=http://<windows-host-ip>:9223 python scripts/vision_driver.py`
Windows: `python C:\tools\chrome-bridge.py --no-launch` (Chrome already
running with `--remote-debugging-port=9222 --user-data-dir=C:\temp\chrome-debug`).

Screenshot ↔ click coordinates were 1:1 (viewport 1920×889, DPR 1). Frames were
read at native resolution via the Read tool.

## What was done (vision only)

1. **Orient** — one screenshot: identified server (InvestiTrade), current
   channel, sidebar layout, that the account cannot post in the channel.
2. **Navigate** — clicked the sidebar entry for `#pre-market-plan` at the
   pixel position seen in the screenshot; URL changed to the expected channel.
   Noticed the view was parked at the "new messages" marker, not the bottom.
3. **Read** — wheel-scrolled to the bottom, then paged up 6× (−650 px per
   step), one screenshot per step. Read 7 frames; transcribed 7 messages
   (Aug 7 → Aug 14, 2026): author, displayed timestamp, full multi-paragraph
   body, ordered-list numbering, channel mentions, reply-to reference,
   attachment type (image / video), reaction counts.
4. **Commit the transcript before looking at ground truth**
   (`data/vision-shots/vision-transcript.json`, gitignored — private server).
5. **Score** against the DOM extractor (`extract` op → `_EXTRACT_JS`).

## Results

| Message | Raw diff ratio | After normalizing DOM-extractor artifacts | Verdict |
|---|---|---|---|
| 8/7 7:09 | 0.848 | **1.000** | identical |
| 8/10 8:18 | 0.991 | **1.000** | identical |
| 8/11 7:31 | 0.994 | **1.000** | identical |
| 8/12 7:44 | 0.990 | **1.000** | identical |
| 8/13 7:38 | 0.993 | **1.000** | identical |
| 8/14 8:06 | 0.992 | **1.000** | identical |
| 8/14 8:14 (reply) | 0.063 | 0.063 | **vision correct, DOM extractor wrong** |

"Normalizing DOM-extractor artifacts" means: strip `1.`/`2.`/`3.` list markers
(the extractor loses them — see bugs), collapse the `,` separators the
extractor emits between list items, and map the raw channel-mention text
`⁠🧠│intraday-commentary` to the rendered `#intraday-commentary`. Every
residual difference on those six messages was the extractor's, not the model's.

On the reply message the extractor returned the *quoted parent's* text; the
vision read (`premarket prep @everyone`, video attachment, reply-to preview)
matches `#message-content-<own id>` in the DOM.

### Where vision was weak

- **Reaction emoji identity** — small glyphs; counts were reliable, the emoji
  itself was a guess in several cases.
- **Chart image contents** — visibly a price chart with annotations, not
  transcribable at 1920px. Would need click-to-expand for image OCR.
- **Relative timestamps** — the two newest render as "Yesterday at 8:06 AM";
  a vision pipeline must resolve them against the capture date. Hovering the
  timestamp reveals the absolute date, at one extra action per message.
- **Throughput** — this channel is one long post + big chart per frame, so
  ~1 message per (scroll + shot + read) cycle. A text-dense channel would give
  5–10 per frame. Still 1–2 orders of magnitude costlier than a `page.evaluate`.

## DOM-extractor bugs found by the comparison (filed as dr-lmr)

Confirmed live against the DOM (`scripts/vision_driver.py` `eval`):

1. **Reply content is the parent's, not the message's.**
   `el.querySelector('[id^="message-content-"]')` matches the reply-context
   preview (`#message-content-<parentId>`) first. Fix: query
   `#message-content-<ownId>` where `ownId` is the tail of `li#chat-messages-<ch>-<id>`.
2. **Author includes timestamp/tooltip text** — `h3.textContent` yields
   `"Carmine Rosato — Yesterday at 8:06 AMFriday, August 14, 2026"`. Fix: use
   `[id^="message-username-"]` (yields the bare name).
3. **`reply_id` is `context-<ownId>`, not the parent id** — the element is
   `#message-reply-context-<ownId>`; stripping `message-reply-` leaves the wrong
   thing. Parent id is available from the preview's `#message-content-<parentId>`.
4. **Ordered-list numbering lost** — Discord renders lists as
   `<ol start=N>`; markers are CSS counters, so `textContent`/`innerText` drop
   them. Needs an `<ol>/<li>` walk to re-emit `N.`.
5. **Attachments not captured** (feature gap, not a bug) — images (`img[src*=attachments]`)
   and `video` elements are present in the `li` and easy to enumerate.

## Recommendation

- **Keep DOM extraction as the primary scraper.** It is exact where it is
  correct, and cheap. Fix the five items above first — the vision pass found
  them in one channel; they affect every reply and every list.
- **Use vision as the navigator / recovery layer**, not the bulk reader:
  finding channels, handling "new messages" markers, dismissing modals,
  detecting when Discord's DOM has shifted under the selectors, and sampling
  a frame per N pages to verify the DOM output.
- **Two-tier read** where fidelity matters: DOM for text, vision to spot-check
  and to describe attachments.

## Plumbing lessons (cost most of the session)

- WSLg did not surface the Playwright Chromium window; the fallback was
  attaching to Windows Chrome over CDP.
- The original `chrome-bridge.py` never called its WebSocket handler —
  DevTools HTTP worked, WS never did. Rewritten as a raw TCP relay.
- A stale `netsh interface portproxy` rule (`0.0.0.0:9222 → 127.0.0.1:9222`)
  on Windows squats the IPv4 port, forces Chrome onto `[::1]:9222` only, and
  makes any IPv4 connection to 9222 loop back on itself (15k TIME_WAIT
  sockets). The bridge now prefers `::1`. Cleanup (admin PowerShell):
  `netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9222`.
- Chrome's `/json/version` advertises `ws://localhost:9222/...`; the driver
  rewrites the host to the bridge address before `connect_over_cdp`.

## Artifacts (local, gitignored)

- `data/vision-shots/*.png` — frames 10–21
- `data/vision-shots/vision-transcript.json` — model transcript, written pre-comparison
- `data/vision-shots/dom-extract.json` — DOM extractor output used as ground truth
