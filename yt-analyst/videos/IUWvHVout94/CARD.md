# Video: IUWvHVout94

- **URL:** https://www.youtube.com/watch?v=IUWvHVout94
- **Title:** Read Liquidity Like a Pro: The 3 Step Strategy That Actually Works
- **Channel:** Trading Notes (@TradingNotes1, 108K subs) — NOT Trade Brigade, see Lessons
- **Uploaded:** 2026-09-04 · **Duration:** 16:08 (968 s)
- **First analyzed:** 2026-09-05
- **Status:** closed
- **Bead:** dr-3kn (grade for clarity + alignment to the corpus)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**Identity — this is not Trade Brigade.** The channel is **Trading Notes**
(`@TradingNotes1`, `UCgljZoL6QzWRzFnfaxRgZ1g`, 108K subscribers), confirmed
by its own on-screen branding card at 13:43 ("Trading Notes 100k
subscribers") and by yt-dlp channel metadata. Trade Brigade is Matt's
newsletter at `tradebrigade.co` (`newsletters/tradebrigade`, bead dr-4ne).
No mention of Trade Brigade appears in this video's title, description,
branding or narration. **Verified: two independent sources (on-screen text
+ channel metadata).**

**Thesis (00:30).** On-screen: `"NOBODY IS HUNTING YOUR STOPS"`. The argument
is that institutional algorithms harvest *resting liquidity* as a mechanical
consequence of needing fill volume, not out of malice toward any individual.
Sourced at 00:20 to an unnamed "particle physicist turned eight-figure futures
trader, 30 years" — the interviewee is never named on screen or in audio.
**Unverified and unverifiable: the appeal to authority is anonymous.**

**The mechanism section (01:05–06:00)** is the strongest part of the video
and is genuinely explanatory:
- *Liquidity* = "resting orders sitting in the market waiting to be
  triggered" (01:05) — two named sources: retail stop losses (01:18) and
  stop-entry breakout orders (01:48).
- Pools cluster above equal highs, below equal lows, along trendlines, and
  at round numbers (02:16).
- The general law, spoken at 02:30: **"Any tool that produces predictable
  behavior produces predictable liquidity."** This is the video's best line
  and its actual intellectual content.
- *Slippage* defined at 03:51; *iceberg orders* at 04:57 (large orders showing
  a small visible fraction and reloading).
- A real Level-2 / Nasdaq DOM depth table is shown at 03:01.

**The 3-step strategy (06:09–08:35) — verbatim, and where it stops short.**

| Step | Title card (verbatim) | Rule given | Precision |
|---|---|---|---|
| 1 | `STEP 1: IDENTIFY THE POOL` (06:09) | Equal highs/lows respected 2–3×, Asian-session extremes, or yesterday's high/low | Adequate |
| 2 | `STEP 2: WAIT FOR THE SWEEP` (06:49) | Price pokes the level, triggers stops, closes weakly or leaves a wick back inside range (07:23) | Adequate |
| 3 | `STEP 3: ENTER ON CONFIRMATION` (07:39) | Drop to lower timeframe, wait for structure shift (ChoCH), enter on the pullback (07:46–08:03) | **Under-specified** |

Stop and target ARE specified: stop "beyond the extreme of the sweep"
(08:05); target "the liquidity pool on the opposite side of the range.
Swept the highs? Target the lows. Swept the lows? Target the highs." (08:08).

Invalidation is specified in three places, which is better than most content
of this type: `NO RESPECT AND MOVE AWAY, NO CONFIRMED POOL` (06:45); stand
aside if the breakout candle body is ≥2× the prior candle, closes far beyond
with a small wick and high volume (07:05–07:16); and the rule card
`NO SWEEP NO TRADE NO EXCEPTIONS` (08:31).

**What is ABSENT (the clarity gap).** Confirmed by dedicated zoom
(runs/20260906-023621):
- **Entry price.** The entry instruction is only "Then you enter on the
  pullback." No pullback depth, no trigger candle, no fib or OB reference.
  Two traders following this video would not enter at the same price.
- **The timeframe pair.** "Your lower timeframe" (07:46) is never given a
  value; the higher timeframe appears only later as a chart badge
  (`30 MIN CHART`, 08:41). The strategy is stated timeframe-agnostically and
  then demonstrated on one arbitrary pairing.
- **Whether the ChoCH needs a candle CLOSE** — never stated. See alignment.
- Undefined-but-used: pullback depth, Asian session hours, the volume-spike
  threshold in the step-2 invalidation.

**The "2 live trades" claim is not supported (08:35–10:35).** The description
promises "2 live trades". What the video shows:
- Dedicated visual zoom found **no TradingView UI at all** — no order panel,
  no broker connection, no account balance, no Bar Replay toolbar, no price
  axis, no ticker watermark, no session clock. The position boxes are plain
  red/green rectangles with **no entry, stop, target or R:R text inside them**.
- The instrument names come from the **spoken audio only**: "the Dow Jones
  futures" (08:39) and "the Nasdaq futures" (09:55). Nothing on screen
  identifies either.
- He never claims personal execution. His own framing: *"show you this
  playing out on a real chart, with a short first"* (08:35) and *"Now, the
  mirror image. This time, a long."* (09:52).
- **No numbers at all** for either trade — no price, no point/tick count, no
  R-multiple, no P&L. Outcomes are described as "a great risk to reward"
  (09:40) and "absolutely monstrous" (09:50).

**Verified by two independent Gemini passes** (a pixels-only pass and an
audio-only pass, each blind to the other's question). Frames were not pulled
— see Lessons. Conclusion: these are **stylized illustrations**, not live
trades and not verifiable replays. The description's wording oversells them;
the narration does not.

**Commercial payload.** This is an affiliate-monetized video, and the product
demo is a substantial fraction of its runtime:
- **11:25–13:40 (~2m15s, 14% of the video)** is a walkthrough of the paid
  **Flux Charts "Price Action Toolkit"** TradingView indicator — settings
  panels at 11:37 (Buyside/Sellside Liquidity, Sensitivity 15, Pivot Length
  25), 12:13 (Liquidity Grabs: Pivot Length 25, Wick-Body Ratio 0.5), 12:47
  (Market Structures: swing length 14, BOS, ChoCH), 13:16 (alert checklist:
  BOS, ChoCH, FVG, IFVG, Order Blocks).
- On-screen `40% PLAN` at 13:47; description: "Labor Day Sale — up to 40%
  off, lifetime plan included, September 4th to 9th", via
  `fluxcharts.com/?via=tradingnotes` — **an affiliate link**.
- Description also carries **two WEEX crypto-exchange referral links**
  (`vipCode=gqnq`, `vipCode=tnotes`, "Up To $30,000 in Rewards") and a
  **TradingView affiliate** (`aff_id=155474`).
- Email capture at 00:54 and in the description: "GET THE FREE BACKTESTING
  GUIDE" → `tradingnotes.live`.
- No price is stated for the Flux Charts product in audio or on screen —
  only the discount percentage.

**Closing section (14:00–15:45).** Three mistakes, as title cards:
`1: PARKING YOUR STOP LOSS IN THE OBVIOUS PLACE.` (14:12);
`2: SELLING EQUAL HIGHS AND BUYING EQUAL LOWS DIRECTLY` (14:38);
`3: TREATING THE SWEEP ALONE AS AN ENTRY SIGNAL` (15:07). Closes on
"It is always better to follow a good process and get a bad result than to
follow a bad process and get a good result" (15:37).

## Grade

**Clarity: B−.** Above average for the genre and clearly written, but it
fails the operator test. Definitions are given and are good; invalidation
rules are explicit and appear three times, which is unusually disciplined;
stop and target logic are stated. But the **entry is not specified**, the
**timeframe pair is not specified**, and the examples carry **no numbers**,
so a viewer cannot reproduce, backtest or falsify the strategy from the
video alone. The irony is direct: the video's own lead magnet is a
*backtesting* guide, and the strategy as taught is not specified tightly
enough to backtest.

**Alignment to the corpus: A−.** This sits squarely in the same
ICT/Smart-Money lineage as the Smart Money Decode X series
(`playlists/smdx-zero-to-advanced-PLU9kIorYkc18.md`) and shares its
vocabulary — liquidity pools, sweeps, BOS/ChoCH, structure shift, HTF/LTF
split. Two specific agreements and one specific gap:
- **Agrees on the sweep/ChoCH distinction.** SMDX v7 warns
  `"1-2 CANDLE SNAP-BACK = LIQUIDITY SWEEP — NOT CHOCH"`. This video's step 3
  requires exactly that ordering — sweep *first*, structure shift *after*,
  as separate events. Independent sources converging on the same
  discrimination is meaningful.
- **Agrees on liquidity as the engine.** SMDX: "every genuine ChoCH is a
  liquidity event: break → stops → collection." Identical mechanism.
- **Gap: the candle-close requirement.** SMDX is explicit that a ChoCH is a
  `"CLOSE BELOW MOST RECENT HL"` — a *close*, not a wick. This video never
  says whether the step-3 structure shift needs a close. That single
  unstated condition is the difference between a rule and a vibe, and the
  corpus already supplies the answer.
- **Weaker than the corpus on timeframes.** SMDX specifies DAILY → 4H →
  1H/15M with swing-qualification minimums (4H = 2, daily = 3). This video
  leaves the pairing open.

**Net.** Worth keeping as a compact, well-narrated statement of the liquidity
premise — 01:05–06:00 and the 02:30 line are genuinely good, and the
mechanism section is better than most of the corpus at explaining *why*
stops get taken. Not worth treating as a tradeable specification. Read the
SMDX synthesis for the parts this video leaves out.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-05 — grade for clarity and alignment (bead dr-3kn).** Wide pass
  (runs/20260906-023508, 88.7K prompt tokens, ~92 tok/s — the expected
  low-rate YouTube-URL path), then three zooms: the 3-step strategy
  (runs/20260906-023621), a pixels-only pass on the two trade examples
  (runs/20260906-023703), and an audio-only pass on the same window. Verdict:
  clarity B−, alignment A−. Established that the channel is Trading Notes,
  not Trade Brigade, and that the description's "2 live trades" are stylized
  illustrations with no prices. Session was interrupted mid-flight by an
  expired Gemini key; the key was rotated and `yta.py env` confirmed it
  (HTTP 200) before the passes ran.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Trading Notes is an affiliate channel.** Flux Charts (`?via=tradingnotes`),
  WEEX (two referral codes), TradingView (`aff_id=155474`), plus an email
  capture at `tradingnotes.live`. Expect a paid-indicator demo of ~2 minutes
  in the back third of any video from this channel; discount windows are
  date-boxed. Read the description before grading — it carries claims the
  video itself does not make.
- **The charts are custom motion graphics, not screen recordings.** No
  TradingView chrome, no axes, no tickers, no prices. Any instrument or
  timeframe attribution for this channel must come from audio or from an
  orange badge overlay (`30 MIN CHART`, `5 MIN CHART`), never from chart
  metadata — there is none to read.
- **Gemini failure mode reproduced here.** The wide pass reported "chart
  displayed using Dow Jones Futures (YM) on 30-minute" as a `visual` claim.
  The pixels-only zoom found no ticker on screen; the audio-only zoom found
  the presenter *saying* "the Dow Jones futures". Gemini had migrated a
  spoken instrument name into an on-screen chart-metadata claim — the
  chart-metadata-invention mode already documented in the SMDX corpus. The
  two-blind-zoom technique (one pass forbidden to look at pixels, one
  forbidden to listen) diagnosed it without frames and is worth reusing.
- Frames were not pulled this session (operator declined the download), so
  no claim here is pixel-verified in the doctrine sense. The two-source
  agreement is strong but is still Gemini twice.
- `yta.py frames` calls bare `yt-dlp`, which is not on PATH — it lives in
  `.venv/bin`. Prepend `.venv/bin` to PATH or the command dies with
  `FileNotFoundError: 'yt-dlp'`.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-023508 [full] gemini-flash-latest (tok 88709/2482) — Q: Map this video end to end for an analyst who has not seen it.

Report:
(1) The c… — runs/20260906-023508/
- 20260906-023638 [06:00-08:45] gemini-flash-latest (tok 15504/1133) — Q: This window contains the video's '3 step strategy'. Transcribe it as an operator… — runs/20260906-023638/
- 20260906-023703 [08:35-11:20] gemini-flash-latest (tok 15567/691) — Q: This window shows two chart examples the video's description calls '2 live trade… — runs/20260906-023703/
- 20260906-025759 [08:35-10:35] gemini-flash-latest (tok 11340/627) — Q: Answer ONLY from the SPOKEN AUDIO in this window. Ignore everything on screen.

… — runs/20260906-025759/
