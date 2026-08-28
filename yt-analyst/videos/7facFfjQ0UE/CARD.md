# Video: 7facFfjQ0UE

- **URL:** https://www.youtube.com/watch?v=7facFfjQ0UE
- **Title:** How To Enter and Exit Trades Like a Professional
- **Channel:** Carmine Rosato — "Trading Orderflow Series" ep. 7 (Gemini's "Invest Trade" is unsupported)
- **Uploaded:** 2024-11-18 · **Duration:** 32:19 (1939 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #8 · bead dr-08s.7
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** Execution: the **CLC rule** — Context, Location,
Confirmation — with confirmation read in "The Now" (live tape/footprint),
never from a candle close. Two journaled trades walked from context to
exit. Platforms (pixel-identified): TradeZella journal
(`app.tradezella.com`, account "Carm - AMP", TradingView chart pane),
Sierra Chart footprints (`ESZ24_FUT_CME[M] 5.00 Range`, "Delta 20t"
replay), thinkorswim/Schwab for candlesticks, Bookmap Replay for heatmaps.

**3 Pillars (01:03–05:56; slides verified at 01:03, 18:35; others
unframed):**
- a. CONTEXT — what is the trend? how is today's volume?
- b. LOCATION — is it at a level of interest? supply/demand or S/R
- c. CONFIRMATION — are buyers buying or trapped? sellers selling or
  trapped?
- Green candle = more aggressive buying than passive selling; red = the
  reverse. "A candlestick chart DOES NOT tell me WHEN to enter or exit.
  The TAPE (volume / orderflow) DOES."

**Timeframes (06:53, verified, a platform dropdown screenshot):** 1D:1m ·
15D:5m · 30D:15m · 90D:30m · 360D:1h · 360D:90m · 360D:2h · 360D:3h ·
360D:4h · 1Y:1D · 3Y:W — used for context and location only.
**"The Now" (07:44–08:27):** the timeframe he trades = live order flow.
"If the market breaks below my support but the volume is more BUYING, I
am getting in LONG right at that moment." A large seller sitting above
resistance and getting filled is invisible on a timeframe chart; "Volume
is read in The Now." (Slides unframed.)

**Trade 1 — ES Thu Oct 3 2024, long (01:26, 09:46–17:33).** TradeZella:
Net/Gross **$21,750.00**, **30**, **14.5** pts, Target **5753.0**, Stop
**5739.0**, Initial Target **$18,750.00**, 5★ (Trade Risk / R fields
behind the webcam; = $2,250 / 8.33R / 9.67R per ep. 2's verified log of
the same trade). **Verified: frames + arithmetic** ⇒ entry **5740.50**,
1.5-pt stop (presenter says "5740, 1-point, ~$2,000–2,200 risk, 9.6:1" —
round-offs).
- Context: uptrend, pullback. Location: demand zone 5743.75→5738 (green
  box). Confirmation (12:29–13:40, Sierra Chart replay from 9:52:08,
  date 2024-10-3): prior bar delta **−735** (vol 951); current bar's low
  cell **−253 | 253** (100 % aggressive selling), then at 9:52:54 delta
  runs −254 → −1100 (900 sell contracts in ~5 s, spoken) and price ticks
  UP — sellers absorbed inside demand ⇒ long at 9:53, stop 1.5 pts below
  the buyer, target the prior high (13 pts). Bookmap Replay (16:21–17:26,
  `03-Oct-2024 09:51:45 (EDT)`, tabs NQZ4/ESZ4@RITHMIC, ESZ4@TM.Lite):
  thick resting-bid band at 5740.25–5741.25; tooltip at 17:03 "09:54 ·
  Bid 5739.75 / Ask 5740.00 · Volume 1739 · Delta −1171" (unframed, but
  identical to ep. 2's −1171 outlier at 5740.00). Rallied "without
  looking back".
- Contrast chart (09:46, thinkorswim): `High Of Day ($5045.25)` with a
  14-row Time & Sales of 100–200-lot sells at 5043.75–5048.25 — a failed
  breakout read from the tape instead of waiting for the 5-min engulfing
  candle. **Verified: frames** (Gemini got 6 of 14 rows wrong by a digit).

**Risk:reward (18:35–21:03).** Slide (verified; bullet 1 genuinely
reads "Waiting for a  to close" — missing word): waiting for a candle
close does not validate strength; "What if a candle closes right at the
level but the volume is still rejecting?"; "What does (time) have to do
with invalidating a trade thesis? Time does not move the market. Volume
– price does." Chart (thinkorswim, /ES 1m, 10/3/24 09:57): the late
entry after the 5-min close risks to the low of day — rectangle
5745.97→5739.16 ≈ **7 pts** — while the order-flow entry risks **2 pts**;
same target (high of day) ⇒ ~1:1 vs ~4:1. Stop principle: where the
thesis is invalidated (low of day). "7pt"/"2pt" labels at 20:18–21:03
unframed. Levels `Price Level13 ($5759.25)`, `Price Level12 ($5753)`.

**Trade 2 — ES Mon Nov 11 2024, short (21:58–30:53).** TradeZella:
Net/Gross **$23,000.00**, **40** contracts, **11.5** pts, Target
**6037.0**, Stop **6046.0**, Initial Target **$15,000.00**, Trade Risk
**−$3,000.00**, Planned **5.00R**, Realized **7.67R**, 5★. **Verified:
frames + arithmetic** (`frames-2155-2205/f_0004.jpg`): 11.5×40×50 =
23,000; risk 1.5 pt ⇒ entry **6044.50**; −7.5 = 6037.0 ✓; 15,000/3,000 =
5.00 ✓; 23,000/3,000 = 7.67 ✓; exit ≈ 6033. (Gemini's "Commissions
$0.00" row does not exist.)
- Context: overnight selling off all-time highs. Location: supply box
  6044.25–6046.00 (Sierra Chart, 2024-11-11, axis 6039–6055). Confirmation
  (28:45–30:53, Bookmap Replay, unframed): a passive seller (thick red
  band at 6045) absorbing green buy bubbles — tooltips "09:33:32 Vol 707
  at 6045.00", "09:39:41 Ask 1140 at 6045.25 / Bid 0 at 6045.00"; delta
  +1900 → +3300 (+1400 absorbed) with no break ⇒ short at 09:41 with a
  1–2 pt stop above the high of day.

**Concrete parameters:** stops 1.5 pts (1–2 pts spoken) beyond the
absorbing participant; targets = the opposing level (7.5–13 pts); 30–40
ES contracts; Sierra Chart 5-point range bars with "Delta 20t"; entries
on the print, never on a candle close.

**Gemini errors caught:** chart-header OHLC "5834/5833 … Volume 24.49K ·
CBOE" — nothing like it on screen (actual 5781.75/5782.50/5779.50/5781.00,
6.044K); "Commissions $0.00" invented; zoom 3 misread stop 5729 and gross
$21,790 (other runs and pixels: 5739 / $21,750); "star outlines" (filled);
Time & Sales 6/14 rows off by a digit; Bookmap tabs "MESZ4" / "@DXTM.Lx-
Lite" (actual NQZ4 / @TM.Lite); `$` dropped from `High Of Day ($5045.25)`;
rectangle coords rounded (5745.97/5739.16 → 5746/5739).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: extract the CLC execution method and verify both
  trade logs. Wide + 8 zooms + 78 frames + Opus verifier (52 tool uses,
  93 min; told to wrap up). Verdict: both logs verified; platforms
  identified from pixels; Gemini's chart-header and Commissions claims
  fabricated. Unframed: 13:20, 17:03, 20:18–21:03, 29:00–30:53 Bookmap.
  Runs: `runs/20260828-122510` (wide), eight zoom dirs `-1228*`…`-1231*`.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- TradeZella panel: Trade Risk / Planned R / Realized R sit bottom-left
  where the webcam bubble lives — pull a frame when he moves, or derive.
- Sierra Chart title bar names the bar type (`5.00 Range`) and contract
  (`ESZ24_FUT_CME`); Bookmap title bar carries the feed (`@TM.Lite`).
- Time & Sales separators are `:` (HH:MM:SS:mmm), not `.`.
- The "candle" word is missing from the risk:reward slide's first bullet
  in the source — not a transcription error.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-122510 [full] gemini-flash-latest (tok 176791/1417) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-122510/
- 20260828-122816 [01:00-02:15] gemini-flash-latest (tok 7127/1279) — Q: Transcribe verbatim the '3 Pillars' slide and every field and number in the trad… — runs/20260828-122816/
- 20260828-122838 [06:45-08:45] gemini-flash-latest (tok 11211/964) — Q: Transcribe verbatim the timeframe table slide (every row: lookback period and ch… — runs/20260828-122838/
- 20260828-122900 [09:30-11:20] gemini-flash-latest (tok 10310/2856) — Q: Transcribe every annotation, label, price level and number on the failed-breakou… — runs/20260828-122900/
- 20260828-122922 [12:15-14:00] gemini-flash-latest (tok 9840/993) — Q: On the footprint replay: transcribe every delta and volume number, price level, … — runs/20260828-122922/
- 20260828-122947 [16:10-17:40] gemini-flash-latest (tok 8467/912) — Q: On the Bookmap replay: platform signatures, instrument (check price axis), times… — runs/20260828-122947/
- 20260828-123009 [18:30-21:10] gemini-flash-latest (tok 14862/960) — Q: Transcribe verbatim the '3 Pillars To My Trading (risk:reward)' slide with every… — runs/20260828-123009/
- 20260828-123112 [21:50-23:40] gemini-flash-latest (tok 10330/1221) — Q: Transcribe every field and number in the short trade's journal panel (date, inst… — runs/20260828-123112/
- 20260828-123127 [28:45-31:00] gemini-flash-latest (tok 12577/852) — Q: On the Bookmap replay near 6045: timestamp string, every price level and number … — runs/20260828-123127/
