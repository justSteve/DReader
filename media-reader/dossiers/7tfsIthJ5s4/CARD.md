# Video: 7tfsIthJ5s4

- **URL:** https://www.youtube.com/watch?v=7tfsIthJ5s4
- **Kind:** youtube
- **Title:** Quant Can Now Control Your Charts
- **Channel:** LuxAlgo (@LuxAlgo)
- **Category:** Trading
- **Uploaded:** 2026-09-21 · **Duration:** 7:57 (477 s) · **Views:** 17,238
- **Bead:** dr-2om
- **First analyzed:** 2026-09-25
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What Quant is (verified: frames).** Quant is an LLM chat assistant built
into LuxAlgo's own web charting app. It is not a TradingView add-on. The URL
bar reads `app.luxalgo.com/quant?workspace=…`, the tab reads `LuxAlgo | Quant`,
and the chart carries LuxAlgo branding, with a LuxAlgo logo where TradingView
puts its own (frames-055-120/f_0003). The look is TradingView-like: left
drawing toolbar, `Indicators` menu, watchlist, `Order Book` and `Alerts` tabs,
`RTH/ETH` toggle. Whether TradingView's charting library runs underneath is
**not established**. The chat sits in a left sidebar with an `Ask for an
indicator` box, a microphone button for dictation and a model picker. The
picker reads `Sol High` in the intro graphic (00:03, frames-001-022/f_0002)
and `Luna Fast High` in the live demo (frames). Those are LuxAlgo's own tier
names, and the models behind them are not disclosed. Footer: *"The assistant
can make mistakes. Verify important information."* The presenter is "Jacob"
(`Welcome back, Jacob`, 00:58).

**What is demonstrated live (verified: frames; all recorded Thu 17 Sep 2026,
23:22–23:49 UTC by the app clock):**
- 01:07 Dictation: *"Hey Quant, can you open up the 15 minute bitcoin
  footprint chart?"* The chart changes from `NQ1! · CME_MINI · 5m` (about
  29,695) to `BTCUSDT · BINANCE · 15m` footprint (about 76,470), and Quant
  replies *"Done — the chart is now set to BTCUSDT on the 15-minute footprint
  view."* (frames-133-225/f_0002). **Symbol, chart type and timeframe
  control: shown.**
- 01:42–02:20 Asked to read the footprint and forecast where the candle closes
  in 13 minutes. Quant replies in about 30 s: *"My base-case estimate is:
  76,420–76,460, with 76,440 as a rough midpoint."* Scenarios: bearish below
  76,420 toward 76,380–76,400; neutral *"between 76,420 and 76,480 and closes
  near 76,440–76,460"*; bullish *"above 76,500–76,520"* toward 76,500+ (sic).
  It hedges: *"a probabilistic footprint read, not a reliable prediction"*
  (frames-133-225/f_0016, 23:31:59 UTC, 13:01 left on the bar).
- 02:54–03:20 Asked for 1h and 4h context. Quant **splits the layout into two
  panes**, 1h and 4h (frames-255-335/f_0010), and writes a top-down read: 1h
  *"near-term momentum fading"*, *"immediate battle is around
  76,350–76,400"*, magnets 76,200 then 76,000; 4h *"corrective recovery, not
  yet a confirmed bullish reversal."* **Layout control: shown.**
- 03:29 Back to one 5m chart. 03:41–04:00 the presenter hand-draws horizontal
  lines at swing highs and lows. 04:04 he asks Quant to *"build me an
  indicator that identifies these key levels… a stop loss and take profit box
  plotted at the closest level that makes the most sense for a bounce."* By
  04:25 an indicator titled **`Bounce Key Levels & Risk Box`** is on the chart
  (frames-420-432/f_0004). Quant lists its defaults: pivot 3 left / 3 right,
  ATR 14, bounce proximity within 1 ATR, stop buffer 0.35 ATR, minimum
  reward/risk 1.2, max 10 levels. It adds: *"it does not place broker
  orders. The setup can update while the current candle develops."*
- 04:40, 05:16, 06:33 Three rounds of revision in plain English, driven by
  what Quant "sees": too many lines across the candles; levels already broken;
  entry not on the level; labels overlapping the lines. Each time the
  indicator is rewritten and reloaded. A `Looking at the chart...` status
  appears (04:52). Whether the code is Pine Script or something else is **not
  shown**. There is a `<>` code icon in the toolbar, but it is never opened.
- 05:57–06:08 The settings dialog has three groups: KEY LEVELS (break
  confirmation buffer 0.1 ATR…), BOUNCE SETUP (ATR 14, proximity 1, stop
  buffer 0.35, min R:R 1.2, box projection 20 bars) and STYLE. The presenter
  hand-edits stop buffer 0.35 → **0.5** and min R:R 1.2 → **1.5**
  (frames-552-610/f_0004, f_0009).

**What is only claimed (unverified, spoken):** *"it can change the timeframe,
the asset, the layout, how many windows it needs to look at"* (00:06), and
all three are in fact shown. *"You no longer have to send it context, it will
get the context itself"* (00:18). *"A major breakthrough in AI trading
technology"* (00:37). *"The future of this is you're going to have an AI
companion"* (07:30). *"Many more like this coming up soon"* (07:41). No
claim of profitability, win rate or accuracy is made anywhere.

**Price and sales: not in the video.** No price, plan, trial or tier is
spoken or shown. The only call to action is *"all the links for all of this
will be in the description"* (07:52). The 00:00–01:15 zoom's claim of an
`Upgrade` button at top right is **false**: the frames show `Journal` and
`Panels` there (frames-055-120/f_0003). The model-tier names suggest
tiered access, but that is inference. What Quant costs was not established
here. It would need the LuxAlgo pricing page, not this video.

**Performance evidence: none, and the one testable forecast went unchecked on
camera.** The presenter abandons the 13-minute forecast at 02:46 to ask about
1h/4h. The later frames do settle it. The 5m bar that opened at 23:45, when
the 15m bar closed, reads `O 76,436.10` (frames-552-610/f_0004, 23:48:44 with
01:16 left on a 5m bar). **So the 15m close was about 76,436. That is inside
the 76,420–76,460 base case, about 4 points under the "near 76,440–76,460"
line.** *(Frames + arithmetic. It assumes the next bar's open equals the
prior close, which is normal on a Binance spot feed but is not shown
directly.)* This is one sample, and the band is 40 points wide around the
live price with 13 minutes to go, on a bar whose range was already about 75
points. Price was at 76,406, below the band, three minutes later (23:34:54,
frames-255-335/f_0010). It is not evidence of skill. The `Backtest` and `Add
alert condition` suggestion chips are visible from 04:26 (frames) and never
clicked.

**The risk box repaints, and the video calls it a feature.** At 06:18: *"when
this candle actually wicked back down from an aggressive sell, it flipped its
position to long, which is really interesting. I was wondering what was going
on."* At 06:53: *"We've had several position changes based on which high or
low it's heading to, which is really cool."* Quant's own note says the setup
*"can update while the current candle develops"* (04:26). A setup that flips
side intrabar has no fixed entry, and any backtest of it would be scored on
hindsight.

**The boxes, checked (frames + arithmetic).**
| When | Side | Entry | SL | TP | Risk | Reward | R:R shown | computed |
|---|---|---|---|---|---|---|---|---|
| 04:26 | short | 76,436.1 | 76,466.1 | 76,323.3 | 30.0 | 112.8 | 3.76 | 3.76 |
| 05:58 | short | 76,510.01 | 76,528.78 | 76,323.37 | 18.77 | 186.64 | 9.94 | 9.943 |

Both close. The chat text agrees with the second box (*"Stop: approximately
76,529 / Target: approximately 76,323 / Reward/risk: about 9.9:1"*). A
9.9:1 box comes from an **18.77-point stop on BTC (0.025%)**, set to 0.35 of
a 5-minute ATR above a pivot. That is inside the spread of one footprint row.
The R:R is an artefact of a tight ATR-fraction buffer, not an edge. (The
04:26 entry is read as 76,436.x from the partly clipped label, and the R:R
check closes at 76,436.1.)

**Footprint data is genuine on this feed.** `BTCUSDT · BINANCE` carries
real aggressor-side trades. The footprint cells (for example `35.2 | 16.5` at
about 76,490, frames-133-225/f_0016) are buy/sell volume in BTC, unlike the
OANDA tick-volume proxy in [fXDBMJFpIaM](../fXDBMJFpIaM/CARD.md). Quant's
line that *"aggressive sell volume [is] leaving roughly 76,480–76,490"* is
consistent with the heavier sell column at that row (my frame read). No
footprint view of `NQ1!` is shown, so whether the app has CME tick data is
unknown.

**Usefulness against the corpus's order-flow method.** Rosato/Vorwald read
the footprint for absorption, trapped participants and acceptance at a
pre-defined location, as it develops (see the it-orderflow cards). Quant's
footprint read is a paragraph of support and resistance bands with three
scenarios. It never names absorption, trapped traders, stacked imbalance or
exhaustion, and it is framed as a close-price forecast, which the method does
not do. Its **useful** parts are these:
- **Chart operation by voice.** Symbol, timeframe, footprint view and
  multi-pane layouts are genuinely hands-free.
- **Fast indicator prototyping from a marked-up chart.** A pivot/ATR level
  tool with editable inputs, built in about 20 s and revised three times.
  That suits building helpers such as prior-day levels or session VAH/VAL
  lines, and presumably a footprint-location marker, all of which you would
  then verify yourself.

It would **not** be good for these:
- Trade signals. There are no stats, the setup flips intrabar, and the
  stops sit inside the noise.
- Replacing the tape read.
- Anything needing a verified backtest, which is never shown.

**The agent-driving-a-chart angle.** The notable part is the loop. Quant
takes a screenshot-level view of the chart, finds its own output wrong from
the pixels (lines across the candles, a broken level still plotted), and
patches its code. The presenter marks the chart with drawings, a circle
and an arrow at 05:09, as the spec, instead of writing requirements. This is
the same "eyes plus a tool surface" pattern as mread.py/Gemini, with the same
trust issue. The user has no verify step apart from eyeballing, and the demo
shows none. There is no code view and no test. The indicator's behaviour
changes while the presenter is speaking and he does not know why (06:18).

**Where Gemini got it wrong (all corrected above by frames).**
- The NQ chart was `5m`, not `30m` as the 00:00–01:15 zoom said.
- There was no `Upgrade` button.
- The wide pass gave the default stop buffer and R:R as 0.25 / 1:2. The
  frames read 0.35 / 1.2. It also said the hand edit was "from 0.25".
- The 05:50 zoom gave break confirmation as 0.5. The frame reads 0.1.
- The 01:35 zoom gave Quant's neutral band as "76,420–76,460". The frame reads
  76,420–76,480, and the bullish trigger 76,500–76,520, not 76,480–76,500.
- The 1h read gave the "immediate battle" as 76,400–76,420. The frame reads
  76,350–76,400. It gave "4-hour consolidation under pressure" where the frame
  reads "corrective recovery". It gave upside 76,500–76,520 where the frame
  reads 76,600–76,800.

None carried an uncertainty flag. The spoken narration was accurate
throughout.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-25 (dr-2om).** Aim: what Quant is, what is live versus claimed,
  pricing, performance evidence, and fit with the order-flow method.
  - Runs: one wide pass (20260925-134845, 43,837 prompt tokens) and five
    clipped zooms (134911, 134929, 134950, 135409, 135416).
  - Frames at 0.5 fps over six windows: frames-001-022, 055-120, 133-225,
    255-335, 420-432, 552-610.
  - Verdict: a real, live demo of an LLM chart assistant in LuxAlgo's own web
    app. Chart control and iterative indicator building are genuine.
  - It makes no performance claims and shows no evidence. The one forecast
    was not checked on camera. Frames show it landed in its 40-point base
    band, which is n=1 and meaningless.
  - The generated risk box repaints intrabar. Price was not in the video.
  - Every chart-identity field and every number in Quant's chat text was
    framed; Gemini misread seven of them.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- The LuxAlgo Quant app is `app.luxalgo.com`, a TradingView-lookalike web
  chart. Do not record it as TradingView. The app clock (bottom right, UTC)
  and the axis date stamp every frame, so recording time is free to establish.
- Quant's answers arrive as long chat panels in the left sidebar that scroll
  off-screen. Gemini paraphrases their numbers into plausible neighbours.
  Frame the panel for every quoted level. The wide pass is only a map here.
- The demo is narrated live and unscripted. The presenter's asides (06:18,
  06:53) carry the most telling information, so run a narration-only zoom
  (prompt: "ONLY the spoken narration") to get them.

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
- 20260925-134845 [full] gemini-flash-latest (tok 43837/2796) — Q: This is a LuxAlgo video about 'Quant', apparently an AI agent that controls Trad… — runs/20260925-134845/
- 20260925-134911 [00:00-01:15] gemini-flash-latest (tok 7102/1526) — Q: Transcribe the narration verbatim with timestamps. Also transcribe verbatim all … — runs/20260925-134911/
- 20260925-134929 [01:35-03:30] gemini-flash-latest (tok 10752/2253) — Q: Transcribe verbatim, with timestamps: the narration, and the full text of each Q… — runs/20260925-134929/
- 20260925-134950 [05:50-07:57] gemini-flash-latest (tok 11855/943) — Q: Transcribe the narration verbatim with timestamps, especially any mention of pri… — runs/20260925-134950/
- 20260925-135409 [03:30-05:50] gemini-flash-latest (tok 12988/1695) — Q: Transcribe ONLY the spoken narration, verbatim, with timestamps, as spoken claim… — runs/20260925-135409/
- 20260925-135416 [06:10-07:57] gemini-flash-latest (tok 9984/1133) — Q: Transcribe ONLY the spoken narration, verbatim, with timestamps, as spoken claim… — runs/20260925-135416/
