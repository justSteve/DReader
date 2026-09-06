# Video: UL5QOCSKnU0

- **URL:** https://www.youtube.com/watch?v=UL5QOCSKnU0
- **Title:** BEST Zero-Lag Indicator On TradingView? I Tested It 8,000 Times & It's FREE
- **Channel:** AlgoTrade Pro (@algotradepro) — affiliate/subscription funnel
- **Uploaded:** 2026-09-04 · **Duration:** 7:40 (460 s) · **Views:** 21,673
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-ljl (grade + assess replicability on our /ES corpus)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What is tested.** `Zero Lag Trend Signals (MTF) [AlgoAlpha]` (01:06, on-screen,
16K users), a free TradingView Pine indicator. Settings shown at 02:08:
**Length 70, Band Multiplier 1.2**; MTF panel defaults 5m/15m/1H/4H/1D (02:07).

**The tested system, verbatim (02:26–02:36, spoken).**
- Entry: *"long trades on bullish flips, short trades on bearish ones."*
- Stop: *"we'll use the most recent swing low or swing high."*
- Exit: *"a hybrid system: we'll close 50% of the position at a one-to-one
  risk-to-reward ratio, move the stop-loss to break-even, and let the
  remaining 50% run with a trailing stop-loss."*

**Test design (04:41, on-screen).** `ALGOTRADE PRO STRATEGY STATS _ ZERO LAG
ALPHA ALGO ON 5-MIN TIMEFRAME (5 ASSETS)`; `All Available Data Since 2020`;
`INITIAL BALANCE $100,000 (without profits compounding)`; symbols
`BTCUSD, XAUUSD, SPX500, TSLA, GBPUSD`; `2% PER TRADE SIGNAL`; engine
`STRATEGY TESTER (TRADINGVIEW)`, executing `ON BAR CLOSE`; baseline
`AVERAGE TRUE RANGE (ATR)`. **"8,000" = trades, not runs** — 00:32 spoken:
*"I'm going to test it on more than 8,000 trades."* The four tables sum to
**8,065**.

### Headline results as presented

| TF | Trades | Winrate | PF | Net % | Max DD % | Sharpe |
|---|---|---|---|---|---|---|
| 5-min | 2,440 | 48.98 | 1.05 | +125.21 | **−75.42** | 4.19 |
| 30-min | 3,060 | 50.26 | 1.11 | +321.64 | −62.90 | 3.30 |
| 1-hour | 2,343 | 51.22 | 1.13 | +290.16 | −62.56 | 2.49 |
| 1-day | 222 | 49.55 | 1.20 | +43.72 | n/s | n/s |

**Arithmetic verification: the tables are internally consistent — the numbers
are real, not invented.** Every derived field reproduces from the gross
figures to 4 decimal places: trade counts sum, winrates match, PF = grossP/grossL,
avg profit/loss = gross ÷ count, avgRR = ratio of those, Net% = (grossP−grossL)
on $100,000, and every Sharpe = (AvgAnnualReturn − 2.00) ÷ AnnualizedVolatility.
Per doctrine, figures satisfying that many independent relations are a coherent
set. **Verified: arithmetic.**

**The arithmetic also corrected a Gemini OCR error.** The wide pass read the
1-day table as `Profit Trades 111 / Loss Trades 112 / Total 223 / Winrate 49,55`.
But avg profit 2367.07 × n = gross 260,377.97 forces **n = 110.000**, and avg
loss 1934.47 forces **112.000**. With 110/112/222, winrate = 49.5495% — an
exact match to the stated 49,55. With 111/223 it would be 49.78%. The true
row is **110 / 112 / 222**. Uniquely determined, no frames needed.

### What the arithmetic breaks

**1. "All Available Data Since 2020" is false for the headline table.** Two
independent routes force the 5-minute test to be **exactly 2.000 years**:
Net% ÷ AvgPerYear = 125.21/62.60 = 2.000, and Trades ÷ SignalsPerYear =
2440/1220 = 2.000. The other tables are internally 6.000 years (30-min:
321.64/53.61 and 3060/510) , 6.000 years (1-hour) and 5.00 years (1-day:
43.72/8.74 and 222/44). So the four timeframes cover **different periods**,
and the banner is wrong for the 5-minute row it sits directly above. Likely
cause: TradingView caps historical bars per plan tier, which bites hardest
on the lowest timeframe — a data limit presented as a date range.

**2. The Sharpe ratios are impossible.** 4.19 on the 5-minute set is
arithmetically consistent with its own inputs — but the input is
`Annualized Volatility 14,48` on an equity curve that draws down **−75.42%**
and whose average drawdown is **−28.30%**. A curve with those drawdowns
cannot have 14.5% annualized vol. Whatever was annualized, it was not the
strategy's return series. A Sharpe above 4 for a **profit factor of 1.05**
is a contradiction in terms: PF 1.05 means gross wins exceed gross losses by
5%. **Ignore every Sharpe in this video.**

**3. Costs are ABSENT and they are the whole story.** Confirmed by dedicated
zoom (runs/20260906-025052): no commission, spread, slippage or fee row
anywhere in the settings. TradingView Strategy Tester defaults to zero.
So these are **gross** results. Expectancy per trade, computed from the
tables:

| TF | Net $ | Trades | Edge per trade | As R (risk $2,000) |
|---|---|---|---|---|
| 5-min | 125,208 | 2,440 | $51.31 | **0.0257 R** |
| 30-min | 321,641 | 3,060 | $105.11 | 0.0526 R |
| 1-hour | 290,156 | 2,343 | $123.84 | 0.0619 R |
| 1-day | 43,717 | 222 | $196.92 | 0.0985 R |

**4. "ON BAR CLOSE" plus a partial-at-1R-then-trail exit is the classic
TradingView intrabar ambiguity.** The tester cannot know whether the 1R
target or the stop was touched first inside a bar. That flaw inflates exactly
this kind of hybrid exit, and it is unquantifiable from the video.

**5. No in-sample / out-of-sample split is stated anywhere** (confirmed,
wide pass). Length 70 and Band Multiplier 1.2 are presented as givens with
no account of how they were chosen.

**6. Even taken at face value the results are untradeable.** +125% over two
years against a **−75% max drawdown**, and two of the five 5-minute assets
lose money (GBPUSD −40.69%, XAUUSD −35.53% — 04:54).

### Pro Tip and ranking

06:06 spoken: *"you can easily add a baseline filter, like a 200 EMA, only
taking longs above it and shorts below."* **This is untested** — it is
offered after the results and changes the tested rules, so no number in the
video applies to it. 06:45 shows the indicator's placement on
`algotradepro.com/indicators-ranking` (`52.33% 195.31% 1114 | 53.44% 192.51%
857 | 55.36% 276.66% 517`) — the channel's own leaderboard, which is also the
product being sold.

### Commercial payload

The video is a funnel to **ATP Signal Engine** (`algotradepro.com/atp-elite-subscription`),
plus affiliates: TradingView (`aff_id=116350`), XTB broker, **Flux Charts**
(`?via=algotrade`, code ATP), AlgoWay, and a Discord. No price stated on screen.
Note the cross-corpus link: **Flux Charts also sponsors Trading Notes**
(`?via=tradingnotes`, [IUWvHVout94](../IUWvHVout94/CARD.md)) — same sponsor
network, two channels, same week.

## Can we test this on our /ES corpus?

**Partly — and the part we can test is the part that matters.** Full analysis
in the Sessions entry; the corpus is `Strader/data/corpus/*/databento_glbx_es.jsonl`
(Databento GLBX.MDP3, schema `trades`, continuous `ES.c.0`).

**What blocks a replication:**
- **Wrong instrument.** They tested `SPX500`, a CFD, not /ES. Different
  spread, tick, roll and session.
- **Wrong span.** They claim 2020→; our ES data starts **2025-05-27**, 269
  usable days (12.2 GB), and two of those are empty.
- **The decisive blocker — intraday coverage.** 233 of 269 days hold only a
  **1–2 hour afternoon fragment** (≈14:00–16:00 ET). Only **22 days** (July
  2026) carry full RTH. The indicator's **Length is 70**: on 5-min bars that
  is 350 minutes ≈ 5.8 hours of warm-up. A 2-hour fragment is **24 bars**.
  The indicator never initialises. On 30-min bars Length 70 needs ~35 trading
  hours; the fragments cannot form continuous 30-min bars at all.
- No overnight/Globex session, so no gap or Asian-session behaviour.

**What we CAN do, and did.** Built 5-min and 30-min ES bars from ticks for the
22 full-RTH July 2026 days (1,628 five-min bars, 273 thirty-min bars) and
measured the **actual distance to the most recent swing** — the video's own
stop rule — then priced it. Round-turn cost taken as **$17/contract**
(1 tick = $12.50, plus ~$4.50 commission); our tick data confirms ES front
month is a one-tick market.

| TF | Median swing stop | Risk/contract | Cost in R | Their edge | Verdict |
|---|---|---|---|---|---|
| 5-min | **7.00 pts** | $350 | 0.0486 R | 0.0257 R | **cost = 1.89× the edge** |
| 30-min | 20.25 pts | $1,012 | 0.0168 R | 0.0526 R | cost = 0.32× the edge |

- **The 5-minute headline result does not survive contact with real ES costs.**
  The stop would have to be **13.2 points** for the stated edge merely to break
  even; the observed median is 7.00. **80.0% of ES 5-min setups are
  negative-expectancy before the first trade is placed.**
- **The 30-minute and 1-hour results do survive costs** — the edge is ~3× the
  friction, and 83.8% of setups have stops wide enough. They remain
  untradeable for a different reason: a −62.90% drawdown at 2% risk.
- This transfers to their SPX500 CFD *worse*, not better: a typical 0.4–0.6
  index-point CFD spread on a 7-point stop is 0.06–0.09 R, above even the
  ES figure.

**Verified: arithmetic (their tables) + our own tick data (the cost test).
Not verified: any replication of their signal generation — we cannot run the
Pine script, and our bars cannot warm it up.**

## Grade

**Clarity: A−.** Genuinely unusual for the genre. The rules are stated
precisely enough to implement (entry, stop, and a fully specified hybrid
exit), the parameters are on screen, the engine is named, the sample is large,
per-asset results are broken out including the two that lose money, and
chapters are marked. This video is *falsifiable*, which is why it was worth
grading. The clarity gap is confined to costs, the missing date range, and
the untested Pro Tip.

**Alignment to the corpus: C.** It is methodologically orthogonal to
everything else we hold. Smart Money Decode X, Carmine Rosato and Trading
Notes all teach *discretionary structure reading* — liquidity, BOS/ChoCH,
order flow — and none of them report a single backtest statistic. This is a
mechanical-signal backtest video that shares no vocabulary and no method with
them. Its one point of contact is negative and useful: it is the only video
in the corpus that puts a number on a signal, and the number says the signal
is worth 1.05 gross and less than 1.00 net at 5 minutes.

**Net.** Keep it as the corpus's cost-of-friction benchmark. The indicator is
free; the finding is that "free indicator with a 48.98% win rate and PF 1.05"
means a losing strategy once ES-grade costs are applied on the timeframe the
title is selling. The 30-minute variant is the only cell here that is not
obviously dead, and its −62.9% drawdown disqualifies it anyway.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — grade + assess /ES replicability (bead dr-ljl).** Wide pass
  plus a spreadsheet zoom (runs/20260906-025052); a first zoom attempt died on
  a 503 cascade into a retired fallback model (see LESSONS.md). Verified all
  four results tables by arithmetic, which corrected a Gemini OCR error in the
  1-day row and exposed the "since 2020" banner as false for the 5-minute
  table (2.000 years, two independent routes). Surveyed
  `Strader/data/corpus` — 269 ES days, 12.2 GB tick data, but 233 of them are
  1–2 hour afternoon fragments against an indicator needing 5.8 h of warm-up.
  Built 5-min and 30-min bars from ticks for the 22 full-RTH July days and
  priced the video's own swing-stop rule: the 5-min edge is 1.89× under water
  on ES; the 30-min edge survives friction. Verdict: clarity A−, alignment C,
  replication impossible, **the load-bearing cost claim tested and refuted**.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **AlgoTrade Pro publishes its numbers in a spreadsheet, so grade it with
  arithmetic, not frames.** Every table here self-validates; the gross P/L
  columns are the key that unlocks trade counts, years covered and per-trade
  expectancy. Always divide Net% by AvgPerYear and Trades by Signals/year —
  that pair exposed the false date banner and costs nothing.
- **Their stat blocks always omit commission and slippage** and use
  TradingView Strategy Tester defaults. Convert every result to expectancy per
  trade in R before believing a profit factor; PF near 1.0 with a low
  timeframe is the tell.
- Treat every Sharpe from this channel as void — the 5-min table pairs
  Sharpe 4.19 with a −75.42% drawdown.
- Channel is a subscription funnel (ATP Signal Engine) whose own
  "indicators ranking" page is the product; the ranked indicator is the video's
  subject. Expect that conflict in every upload.
- **Flux Charts sponsors this channel and Trading Notes both** — the same
  affiliate network runs across at least two channels in this corpus.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-031400 [full] gemini-flash-latest (tok 42513/2938) — Q: This video claims to have backtested a TradingView indicator 8,000 times. Extrac… — runs/20260906-031400/
- 20260906-031943 [04:19-05:05] gemini-flash-latest (tok 4625/1639) — Q: Transcribe the on-screen spreadsheet in this window CELL BY CELL, verbatim, exac… — runs/20260906-031943/
