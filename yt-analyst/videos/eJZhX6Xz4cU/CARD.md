# Video: eJZhX6Xz4cU

- **URL:** https://www.youtube.com/watch?v=eJZhX6Xz4cU
- **Title:** STOP Using Candlestick Charts, Use This Instead
- **Channel:** Carmine Rosato (Jumpstart Trading) — "Trading Orderflow Series" ep. 2
- **Uploaded:** 2024-10-18 · **Duration:** 24:53 (1493 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #3 · bead dr-08s.2
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** Reading completed transactions instead of candles:
Time & Sales → footprint charts → delta → his 3-column custom footprint on
Sierra Chart → two reversal setups (trapped aggressors; volume tail on a
failed breakout). Reuses ep. 1's auction summary slide at 05:49.

**Time & Sales (06:24–07:53).** Slide: shows COMPLETED transactions; a buyer
and seller to every transaction; identifies the AGGRESSOR. Nine-row example
(Time | Price | Size), prices 5538.50–5541.25, sizes 50–130; the highlighted
print **09:30:11:072 · 5539.25 · 130** (red) = 130 contracts sold at market
into passive bids. **Verified: frames** (`frames-745-815/f_0005.jpg`, 7:53)
— all nine rows text-exact. **Disagreement, unresolved:** row 6
(09:30:00:138 · 5538.75 · 51) — Gemini red, Opus verifier reads green in two
frames (`f_0003.jpg`, `f_0005.jpg`). Green would mean a buyer lifted the
ask. Steve to adjudicate; low stakes for the lesson.

**Footprint anatomy (08:08).** Left of the × = market sells hitting the bid,
right = market buys lifting the ask; shows completed transactions in real
time. Ladder 5724.00–5729.00 (21 rows, 0.25 steps), e.g. 5726.75 = 1581 ×
1398 (the high-volume node), 5729.00 = — × 1. **Verified: frames** — 17/21
rows exact; Gemini misread 4 cells (5728.50 `9×45` read as `17×27`; 5726.50
`886×972` as `890×813`; 5725.75 `522×763` as `411×363`; 5724.75 `270` as
`271`). Same static ladder is reused on the 11:16 slide.

**Delta (11:16, 13:06).** `Delta = ask volume − bid volume`; examples 51−1 =
+50, 2−102 = −100. Comparison ladder (bid × ask → delta): 75×197→122,
1253×1145→−108, 522×1147→625, 1128×1737→609, 3104×3109→5, 2251×3027→776,
3759×1729→−2030, 190×0→−190. **Verified: frames + arithmetic** (all eight
rows satisfy the formula; slides word-perfect).

**His footprint layout (13:32–15:38), Sierra Chart, ES, 20-tick = 5-point
RANGE bars** (spoken; corroborated by frames — every bar on the 17:41 chart
spans exactly 21 rows = 20 ticks; unequal time-axis spacing confirms range
bars):
- Column #1 — TOTAL VOLUME at price, shaded by distribution (`84 = 84 total
  volume`); used to see lack of interest vs fair value.
- Column #2 — DELTA at price (`+84 = 84 hit ask, 0 on bid`; `+216 = 216 more
  aggressive buyers`); used to gauge aggression. Colors: positive blue,
  negative red.
- Column #3 — volume profile colored by delta, distributed by total volume.
**Verified: frames** (`frames-1330-1540/`), slides exact; the example
footprint's 21 delta/volume pairs all share parity (a necessary condition
of delta = ask − bid), so the verifier's transcription is near-certain.

**Rule — trapped participants (16:14).** Lots of aggressive participants at
a price with NO follow-through ⇒ possible reversal. Strong selling but
market not moving lower ⇒ a passive buyer is active; with context those
sellers get trapped when price lifts. **Verified: frames** (slide exact).

**Trade example 1 (17:26–18:54), ES Thu Oct 03 2024, long.** Journal (TradeZella-
style UI on a TradingView 1m chart): Net/Gross P&L **$21,750.00**, **30**
contracts, **14.5** points, Profit Target **5753.0**, Stop **5739.0**,
Initial Target **$18,750.00**, Trade Risk **$2,250.00**, Planned
**8.33R**, Realized **9.67R**. **Verified: frames + arithmetic** — all six
figures literally on screen (`frames-1720-1755/f_0004.jpg`); 14.5×30×50 =
21,750; 18,750/2,250 = 8.33; 21,750/2,250 = 9.67; risk ⇒ 1.5-pt stop ⇒
**entry 5740.5** (derived, not displayed) ⇒ 5753−5740.5 = 12.5 pts = $18,750.
Setup: delta outliers **−735** (9:44:47 bar, ~5740.50) and **−1171**
(9:51:47 bar, ~5740.00) printed AT the session low with no downside
follow-through ⇒ aggressive sellers absorbed ⇒ long at 5740.5, stop 1.5
below, target +12.5; exit ≈ 5755 (beyond target). Slide 18:32 contrasts the
plain candlestick view: "Can you see anything from this chart??"
*Gemini's zoom misread two fields ($14,750 / 6.33R); the wide pass and the
pixels agree on $18,750 / 8.33R, and only that set closes the arithmetic.*

**Setup 2 — volume tail on a failed breakout (21:37–23:26).** Chart labelled
`RESISTANCE HIGH (5733.5)`; slide: "This looks bullish right? Strong
breakout, large green volume bar." As price breaks out, volume dissipates;
at the extreme high the footprint tapers to tiny prints (Gemini: 22×26 then
0×0 at 5735.00–5735.25, 10:45:11 bar) = the tail = no buyers above
resistance ⇒ sellers must lower price; when delta turns red (aggressive
sellers) enter short against the high. No explicit stop/target given.
**Unverified** (no frames pulled for 21:00–23:40).

**Concrete parameters:** Sierra Chart; ES; 20-tick/5-pt range footprint;
3 columns (volume, delta, delta-colored profile); risk 1.5 pts on trade 1.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: extract the footprint method and verify every number.
  Wide pass + 4 zooms (07:20–08:50, 13:20–15:50, 17:10–19:00, 21:00–23:40) +
  67 frames + Opus verifier. Verdict: slides exact; dense ladders ~80%
  accurate per cell; trade log verified to the cent with one zoom misread
  caught by arithmetic before frames. Open: row-6 color, volume-tail window
  unframed. Runs: `runs/20260828-110445` (wide), `-110622` (T&S),
  `-110709` (columns), `-110750` (trade log), `-110838` (tail).

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Trade examples come from a journal UI (Playbook / Trade Rating /
  Executions tabs, TradingView chart) — every risk figure is displayed, so
  provenance is checkable; entry price is NOT displayed and must be derived
  from stop + risk.
- Footprint ladders are 21 rows per bar; Gemini's per-cell error rate on
  them is ~1 in 5 — use the parity check (delta ≡ volume mod 2) and
  delta = ask − bid before trusting any cell, or pull frames.
- Slides are static screenshots reused across the episode (08:08 ladder =
  11:16 ladder).
- Red hand annotations accumulate; the journal's chart legend can show a
  stale crosshair OHLC outside the visible range — ignore it.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-110445 [full] gemini-flash-latest (tok 136185/1720) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-110445/
- 20260828-110622 [07:20-08:50] gemini-flash-latest (tok 8488/2591) — Q: Transcribe verbatim the Time and Sales window shown: every visible row (time, pr… — runs/20260828-110622/
- 20260828-110717 [13:20-15:50] gemini-flash-latest (tok 13961/961) — Q: Transcribe verbatim the three 'My Personal Footprint Chart' column-definition sl… — runs/20260828-110717/
- 20260828-110750 [17:10-19:00] gemini-flash-latest (tok 10326/1105) — Q: Transcribe verbatim every field and number in the trade log shown (P&L, contract… — runs/20260828-110750/
- 20260828-110823 [21:00-23:40] gemini-flash-latest (tok 14861/617) — Q: Paraphrase precisely the failed-breakout / volume-tail reversal setup the presen… — runs/20260828-110823/
