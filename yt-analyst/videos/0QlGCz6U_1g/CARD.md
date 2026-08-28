# Video: 0QlGCz6U_1g

- **URL:** https://www.youtube.com/watch?v=0QlGCz6U_1g
- **Title:** STOP Thinking Like A Retail Trader, Start Trading Like An Institution
- **Channel:** Carmine Rosato — "Trading Orderflow Series" ep. 4
- **Uploaded:** 2024-10-29 · **Duration:** 16:25 (985 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #5 · bead dr-08s.4
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** Mindset episode: retail buys breakouts/dips and sells
panics; "smart money" does the opposite — buys at *wholesale* (demand,
panic, stop hunts) and sells at *market price* (supply, breakouts). Retail
is the liquidity ("bait fish"). Few parameters; the actionable content is
the stop-hunt read at 08:53 and the rules slide.

**Slides (all verified word-for-word by frames unless noted):**
- 01:02 *Retail vs. Institutions* — retail = struggling, less profitable;
  smart money profits from retail; provide liquidity; Buffett: "a device for
  transferring money from the impatient to the patient".
- 02:35 *Goldman Sachs 2012* — 236 profitable days / 15 losing; 41 days >
  $100M; 112 days $50–100M; $18.1B = 53% of revenue from sales & trading
  (Bloomberg text). Histogram "Daily Trading Net Revenues, $ in millions":
  <(100)=0, (100)-(75)=0, (75)-(50)=2, (50)-(25)=2, (25)-0=12, 0-25=27,
  25-50=56, 50-75=75, 75-100=37, >100=41. **Verified: frames + arithmetic**
  (27+56+75+37+41 = 236 ✓; 75+37 = 112 ✓; >100 = 41 ✓; losing bars sum to
  16 vs headline 15 — inconsistency in the source graphic). External claim
  not independently checked.
- 03:38 *How Does Retail Trade?* — buying when they should sell and vice
  versa; "how many times have you stopped out … and then the market moves
  in your favor?" (second bullet appears 04:56; slide shown twice).
- 07:07 → 09:39 *Trade Like Smart Money* — builds progressively; full list
  by 09:39: don't think conventionally; ALWAYS know who is on the other side
  of your trade; market vs wholesale prices; place orders when smart money
  is active; profit from those areas. **Header verified at 07:07; full list
  unverified** (no frames at 09:39; Gemini's wide pass reported the full
  list at 07:07 when only the header was up).
- 10:04 *Stop Thinking Conventionally* — "Would you buy at this green box?"
  vs four retail objections (price falling, lower lows, buying after a
  crash is bad, bad earnings) → the green box is *Demand*. Chart axis
  2908–2940 with Wed/Thu dividers (instrument unknown).
- 12:20–12:52 *Supply = Market Price, Demand = Wholesale*; *Why Does Price
  Change Directions?* — when price rallies retail buys where institutions
  sell; when it drops retail sells where institutions buy; retail provides
  liquidity for large orders; "retail are the bait fish". **Unverified**
  (no frames).
- 14:05 *bait-fish diagram* — bullets: the auction is dynamic; retail and
  big money ARE the auction; big money must stay ahead of retail to get
  filled — if they need to BUY they want RETAIL to SELL and vice versa;
  "we are their bait — outsmart the fisherman". Diagram: BIG MARKET PLAYERS
  (bank icon with fishing rod), ~13 fish each labelled STOPLOSS, two SUPPORT
  LEVEL lines at different heights, candles dipping through the lower one
  then rallying. **Verified: frames** (Gemini omitted every STOPLOSS label).

**Chart examples (ES, 1-min, ThinkorSwim-style, ticker/timeframe never on
screen):**
- 03:51 *breakout trap* — white resistance line at 5830 (last 5831, MA
  5827.2), demand zone `Price Level12 ($5814.75)`; rally to 5830 at 09:55,
  rejection 09:57, pullback to MA, real break ≈10:09. Retail buys the first
  touch and is stopped on the pullback. **Verified: frames**
  (`frames-350-540/f_0001.jpg`).
- 05:25 *trendline trap* — `RESISTANCE ($5730)` label, sell-off from 5750
  to ≈5725 at 09:44, V-reversal to 5746, shallow ascending trendline from
  the 09:51 low; text box "Long the market when it is holding this trend
  line" → (06:05) "Stops you out for a loss". **Verified: frames** (06:05
  update unverified).
- 06:10–07:06 *"Buying every single move up or down"* — same session
  scrolled to 10:50, five circled candles. **Missed entirely by the wide
  pass; found by the verifier** (`frames-705-715/f_0001.jpg`).
- 08:53 *stop hunt in order flow* — **Bookmap** (heatmap + volume-dot
  bubbles + replay controls; no logo) with a DOM ladder (VPS|VPB|Bid|RB|RA|
  Ask|Price|VPD|SVP), tabs ESZ4/NQZ4 @RITHMIC, **displayed instrument ES**
  (axis 5733–5754), `02-Oct-2024 10:03:39.368 (EDT)`; same session as the
  trendline chart. Read: red (sell) bubble stream from ≈5747 at 09:58 down
  to ≈5741 at 10:01, largest at 5743–5744 = retail stopped out under the
  trendline; immediately a column of large green bubbles from ≈5742 to
  5754.5 = smart money buying wholesale. Presenter draws an entry line at
  ≈5742 (no number written). **Verified: frames** (`frames-850-940/`).
  Rule: prefer getting long IN the stop hunt (wholesale) rather than when a
  trendline "holds".

**Concrete parameters:** none numeric. Next episode (15:39): support &
resistance — fakeouts vs continuation.

**Gemini errors caught:** `NQZ4 (CME) 250 Vol` (read an inactive tab; chart
is ES; "250 Vol" not visible); `10:03:39 PM EDT (+00)` (milliseconds
`.368` rendered as PM/offset); `RESISTANCE (151759)` (label fusion; actual
`RESISTANCE ($5730)`); `Price Level12 (5814.9)` (actual `($5814.75)`);
07:07 slide reported fully built (only header up); STOPLOSS labels and the
06:10 chart segment omitted.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: extract the mindset rules and verify slides/charts.
  Wide + 3 zooms (03:35–06:10, 08:40–10:00, 12:20–16:00) + 46 frames + Opus
  verifier (38 tool uses, 30 min). Verdict: slides exact; chart text and
  metadata unreliable (instrument, timestamp, labels); one chart segment
  missed by the wide pass. Card closed. Runs: `runs/20260828-113545` (wide),
  `-113811`, `-113856`, `-113926` (zooms).

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Chart screenshots carry NO ticker/timeframe; instrument tabs in Bookmap
  list several contracts — read the price axis, not the tabs.
- Slides build progressively over minutes; a wide-pass timestamp for a
  slide is its FIRST appearance, not when the full text is up.
- Bookmap timestamps include milliseconds (`HH:MM:SS.mmm (EDT)`).
- The same ES session (02-Oct-2024, `RESISTANCE ($5730)`) is reused across
  three chart examples; ep. 3's Oct 02 trade log is this session.
- Webcam bubble bottom-left occludes the last lines of long slides.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-113545 [full] gemini-flash-latest (tok 89968/1142) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-113545/
- 20260828-113702 [03:35-06:10] gemini-flash-latest (tok 14398/978) — Q: Transcribe verbatim all text on the 'How Does Retail Trade?' slide and every lab… — runs/20260828-113702/
- 20260828-113715 [08:40-10:00] gemini-flash-latest (tok 7583/774) — Q: Describe the order-flow chart shown: platform (any logo or UI text), instrument,… — runs/20260828-113715/
- 20260828-113728 [12:20-16:00] gemini-flash-latest (tok 20317/1261) — Q: Transcribe verbatim every slide shown (supply/demand, 'Why Does Price Change Dir… — runs/20260828-113728/
