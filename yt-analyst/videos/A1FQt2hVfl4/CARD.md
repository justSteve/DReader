# Video: A1FQt2hVfl4

- **URL:** https://www.youtube.com/watch?v=A1FQt2hVfl4
- **Title:** Simple Way to Find Trapped Buyers and Sellers on the NQ and ES
- **Channel:** Trader Rob (robstrades.com)
- **Uploaded:** 2026-08-28 · **Duration:** 42:28 (2548 s) · **Views:** 3,770
- **Playlist:** none (standalone paste, 2026-09-10) · bead: dr-y1k (filed by COO after the beads witness repair, 2026-09-10)
- **First analyzed:** 2026-09-10
- **Status:** open

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**Wide pass only (2026-09-10). Nothing below is frame- or arithmetic-verified yet;
every item is Gemini's read of the whole video at default sampling.**

**What it is.** A ~42-minute method lecture: how to spot trapped buyers and
sellers at pre-marked intraday levels on NQ and ES, shown three ways with
increasing order-flow detail — naked candlesticks, volume bubbles, footprint.
Same skeleton each time: mark levels → wait for a setup candle at a level →
enter on the trigger candle → minimum 1:1.5 R. Historical chart replays, not
live trades; no P&L figures are stated anywhere (unverified — none surfaced).

**Structure.**
- 00:00 title card "Trapped Buyers & Sellers", TraderRob branding.
- 01:06 slide "3 WAYS TO TRADE — 1 Naked Charts · 2 Volume Bubbles · 3 Footprint Chart".
- 02:51–03:16 Step 1, the price levels to mark daily: Prior Day High, Prior Day
  Low, Daily Open, Session High + Lows.
- 04:09–05:55 the volume levels: Pre-Session POC/VAH/VAL, New York Session
  POC/VAH/VAL, and "Unbalanced Volume" areas.
- 07:34 Step 2, setup candle timeframes for naked charts: **NQ 5M → 1M, ES 15M → 5M**
  (higher timeframe for the setup, lower for the trigger).
- 13:29 execution rules, naked charts: **entry at 50 % of the trigger candle,
  min 1:1.5 RR**; 13:30 stop at the setup candle's low wick for a long.
- 16:52 spoken worked example of the R rule: a $100 stop needs a $150 target.
- 17:03 method 2, Volume Bubbles; 18:49 same timeframes as naked charts; 22:50
  same entry/RR rule.
- 23:53 method 3, Footprint; range-bar settings on screen: **"NQ 60R – 30R |
  ES 4R – 12R"** (see zoom candidates — the ES order is reversed relative to
  NQ and may be misread).
- 27:03 footprint setup rule: a green setup candle with **negative total delta**
  qualifies for a long (sellers hit into it and lost — trapped sellers).
- 28:08 footprint entry; 28:40 min 1:1.5 RR.
- 30:28 live-platform walkthrough on NQ with levels labelled: "TraderRob Key
  Level 29809.50", "Prior Day High 29708.00", "Today's Open 29635.50".
- 36:44 volume bubbles on a 5-minute NQ chart.
- 38:34 30-range footprint chart with volume profile and per-candle delta.
- 40:12 spoken: a candle "closed down despite a positive delta of 92" — the
  trapped-buyers illustration.
- 42:11 outro, WWW.ROBSTRADES.COM.

**Numbers stated (all unverified).** 1:1.5 minimum R (13:29, 22:50, 28:40);
$100 stop / $150 target (16:52); NQ levels 29809.50 / 29708.00 / 29635.50
(30:28); delta +92 on a down-closing candle (40:12); range settings NQ 60R/30R,
ES 4R/12R (23:53).

**Zoom candidates.**
- 23:53 ±10 s — settle the ES range-bar pair (4R–12R vs 12R–4R) and confirm NQ 60R/30R.
- 30:28 ±30 s — Gemini flagged the ladder digits as compressed; confirm the three level prices and identify the platform.
- 38:34–40:30 — the footprint example: confirm the +92 delta and that the candle closed down; Gemini listed the delta as spoken, not on-screen.
- 13:29–13:40 — stop placement and the 50 % entry rule as drawn, not just as slide text.

**Uncertainties Gemini declared.** Platform not named on screen (it guessed
Sierra Chart or Quantower); ladder and sub-tick delta figures at 30:28 and
38:34 partly unreadable at this sampling.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- 2026-09-10 — Steve pasted the URL (not previously in the corpus). Wide pass
  only, defaults, 232,206 prompt tokens. Verdict: clean structural map with
  slide text captured; no numbers verified yet. Zooms deferred to Steve.
  Run: runs/20260910-071319.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- First Trader Rob card in the corpus. Format is slide-driven: method rules are
  stated as short on-screen text ("Step 2 – Setup Candle", "Min. 1 to 1.5 RR")
  and repeated for each of the three methods, so slide text is cheap to verify
  and the rule set is small.
- Dense data lives late: platform walkthrough from ~30:28, footprint from
  ~38:34. Everything before ~30:00 is slides and hand-drawn examples.
- Platform unidentified by Gemini; likely Sierra Chart or Quantower. Uses
  range bars (R) for footprint, minute bars for the other two methods.
- Thematic overlap with the Carmine Rosato orderflow series (trapped traders,
  absorption) — cross-link once findings are verified.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260910-071319 [full] gemini-flash-latest (tok 232206/1568) — Q: Give a complete map of this video: title, channel/presenter, what it is about, i… — runs/20260910-071319/
- 20260910-072800 [23:30-24:40] gemini-flash-latest (tok 6667/734) — Q: Transcribe verbatim every line of on-screen text in this window, especially the … — runs/20260910-072800/
