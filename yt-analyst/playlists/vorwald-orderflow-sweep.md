# Channel sweep — Tom Vorwald EN / WorldClassEdge, order-flow & volume seam

- **Channel:** https://www.youtube.com/@tom_vorwald_en (`@tom_vorwald_en`, 93 uploads)
- **Analyzed:** 2026-09-06 · epic bead `dr-zk8` · cards in `videos/<id>/CARD.md`
- **Scope:** the 19 uploads whose titles sit on the order-flow / volume /
  profile / VWAP / PbD axis, selected from all 93. **10 completed; 9 blocked**
  by a Gemini free-tier daily quota — see *Coverage and what is missing*.
- **Method:** one standardised order-flow wide pass per video, the *identical*
  question across every video so the answers are directly comparable. No
  zooms: the sweep is for breadth, and the quota stopped further calls.

## Coverage

| # | Video | Title | Len | Card | Pass |
|---|-------|-------|-----|------|------|
| 1 | `vl01TiVTuoQ` | Master Orderflow Trading: Ultimate Step-by-Step Guide | 12:03 | closed | ✔ |
| 2 | `usho6UVLqkE` | The Orderflow System that 95% of Traders do NOT know | 17:43 | closed | ✔ |
| 3 | `RwQBdF9TSvc` | Wall Street scalper: The Truth about order flow Trading | 33:47 | closed | ✔ |
| 4 | `Vd83oo_geMk` | THE TRUTH about Heatmap & Liquidity | 15:13 | closed | ✔ |
| 5 | `K8qtT2_axPo` | Market Profile: How World Champions REALLY read the Market | 16:25 | closed | ✔ |
| 6 | `1utSjHs_Mq8` | The ONLY Market-Profile-Video you will EVER need | 15:06 | closed | ✔ |
| 7 | `NkQeOVDTAec` | The ONLY Volume-Profile-Video (World Champions) | 9:33 | closed | ✔ |
| 8 | `YmygDgtoxO8` | The ONLY Volume-Profile-Video (World Champion) | 13:49 | closed | ✔ |
| 9 | `aursfDVYzUk` | The perfect trade entry with THIS volume analysis | 18:29 | closed | ✔ |
| 10 | `0CrkbfuIhkc` | Crash or All-In? What Volume Profile Tells Us NOW | 14:12 | closed | ✔ |
| — | `YkclL6xgu-s` | How powerful is Volume Trading REALLY? | 13:00 | — | quota |
| — | `43JaKHRvxHk` | 90% of Traders Use VWAP WRONG! | 10:41 | — | quota |
| — | `VumVuGnCcFM` | The ONLY VWAP-Video you will EVER need | 11:59 | — | quota |
| — | `Ly62G168MkQ` | The Simplest Day Trading Strategy (PbD Method) | 16:10 | — | quota |
| — | `jXR1afMy-3o` | PbD: The World's BEST trading strategy | 12:08 | — | quota |
| — | `m3IMdc7QwN4` | PbD: BEST strategy for times of crisis | 9:18 | — | quota |
| — | `Kg6sYKgtkrY` | The ONLY Strategy you need for 2026 (PbD Method) | 15:41 | — | quota |
| — | `yWO8hVpRXeY` | LIVE DAY TRADING — PbD on the DAX Future | 17:56 | — | quota |
| — | `uFxYcpiaOpw` | My Simplest Trading Strategy (80–90% Win Rate) | 9:33 | — | quota |

Two further videos from this channel were carded earlier in the same session
and belong to the same body of work: [`zAwEX_tRUfE`](../videos/zAwEX_tRUfE/CARD.md)
(1-minute scalping, prior-day Value Area) and
[`HySZZSjMxF8`](../videos/HySZZSjMxF8/CARD.md) (multi-timeframe, volume
exhaustion).

## The method, assembled across the sweep

**Premise.** Price is an auction; the order book is the market. Order flow is
defined once, cleanly, and it is the best single line in the corpus
(`vl01TiVTuoQ` 00:42):

> *"Orderflow doesn't just show you where prices were, but who is currently
> buying, who is currently selling, and how aggressively."*

**Instruments he reads.** DOM/order book (20 levels default, settable to 100),
footprint/cluster charts with a delta histogram, volume profile (composite and
periodic), and Market Profile/TPO. Platforms vary by video and must not be
assumed: **VolFix** (`K8qtT2_axPo` watermark), **VolaTrader**
(`YmygDgtoxO8` © 2023), **TradingView** (`0CrkbfuIhkc`, `HySZZSjMxF8`),
**ATAS on dxFeed** (`zAwEX_tRUfE`), plus a German-language DOM execution panel
(`Kauf`/`Verkauf`, `vl01TiVTuoQ` 06:08). Teaching is almost always done in
**MS Paint** over static screenshots.

**Market Profile vocabulary** (`K8qtT2_axPo`, `1utSjHs_Mq8`) — the fullest in
the corpus. Steidlmayer, 1980s, soybeans; 30-minute TPO blocks; initial
balance = the opening 30 minutes; normal/balanced profile = bell curve; normal
variation = balanced but rejected on one side; double distribution = two
profiles split by single prints; single prints = swift moves by strong
participants; **buying/selling tails** = single letters at the bottom/top;
**ledgers** = multiple letters ending at one price, meaning weak hands.

**Volume Profile vocabulary** (`YmygDgtoxO8`, `aursfDVYzUk`). POC = highest
accumulated volume at a price. VAH/VAL = **where the market starts moving into
imbalance** — a sharper framing than the usual "70% container". Unfair price =
everything outside the value area. LVN = low-volume node. Value area basis is
given as **68.2% (one standard deviation) or 70%**, and naming 68.2% is a
precision no other corpus source offers.

**The distinction the rest of the corpus lacks: POC vs VPOC.** `K8qtT2_axPo`
(05:34) separates the *time*-weighted point of control from the *volume*-
weighted one. `1utSjHs_Mq8` (06:45) then supplies the payoff — **the anomaly**,
where the highest-volume price diverges from the highest-time-spent price.
Carmine and SMDX both use "POC" loosely; this is a real analytical improvement.

**Signals.**
- **Absorption** (`usho6UVLqkE` 14:24): a buyer repeatedly lifting a level with
  price failing to advance, because a large seller is absorbing.
- **Front-running** (`usho6UVLqkE` 09:19): a large resting order acts as a
  **magnet**; price is drawn toward it. **New to the corpus** — Carmine fades
  absorption but never trades *toward* resting size.
- **Iceberg** (`Vd83oo_geMk` 14:10): a large order continuously absorbed and
  refilled without price moving.
- **Weak highs/lows** (`1utSjHs_Mq8` 09:30): extremes built by retail carry a
  high probability of being revisited and broken.
- **Volume exhaustion** (`HySZZSjMxF8` 10:43): volume spikes at a pre-located
  extreme, then price trades back below where the increased volume began.

**The one near-tradeable rule in the sweep** (`1utSjHs_Mq8` 10:54): if price
re-enters a previous value area **and finds acceptance**, there is a high
probability it traverses the **full profile**. Trigger, condition and target.

**Entry model** (`NkQeOVDTAec`): **Idea and Proof.** The Idea is a price level
from the profile; the Proof is a local setup — *"a price, volume or footprint
formation that reduces risk"* — and the trigger is a **pullback to the setup
range after a breakout**. Note this is Carmine's break-and-retest, not the
entry-on-the-break taught in `zAwEX_tRUfE`.

## The numbers — what this sweep adds that the corpus did not have

The Carmine synthesis records, explicitly, that the series never specifies a
numeric threshold, a position-sizing rule, an exit rule **or any win rate**.
This sweep closes several of those gaps:

| Quantity | Value | Source |
|---|---|---|
| "Truly large" resting order, ES | **> 250–300 contracts** (or 400/500/600) | `Vd83oo_geMk` 02:44 |
| Genuinely large ES book activity | **10,000 contracts** bought | `RwQBdF9TSvc` 17:10 |
| Trades needed for reliable statistics | **200–300** | `NkQeOVDTAec` 06:58 |
| Planning hit rate | **50%** | `NkQeOVDTAec` 07:03 |
| Target average risk-reward | **> 2** | `NkQeOVDTAec` 07:18 |
| Break-even win rate at R:R 0.8 | he says ~60%; true value **55.56%** | `zAwEX_tRUfE` 04:48 |
| Market in balanced/sideways phases | **~70% of the time** | `K8qtT2_axPo` 10:41 |
| Market returns to fair value | **~70% of phases** | `YmygDgtoxO8` 05:51 |
| Value area basis | **68.2% or 70%** | `aursfDVYzUk` 06:31 |
| Institutional routing time for size | **1.5–2 days** | `aursfDVYzUk` 03:17 |
| Order-book depth lost in a COVID-scale event | up to **80%** | `RwQBdF9TSvc` 26:04 |
| DAX spread under that stress | **20 points** | `RwQBdF9TSvc` 26:17 |
| Euro Stoxx depth under stress | **300–500 → single digits** | `RwQBdF9TSvc` 26:23 |

**Arithmetic check on the framework.** At the stated 50% hit rate the
break-even risk-reward is exactly **1.00**, so a target of R:R > 2 implies an
expectancy of **+0.50 R per trade**. The framework is internally coherent and
leaves real margin — it is not a knife edge. It is also the only place in this
entire corpus where a win rate and a risk-reward target are stated together.

**Per-instrument book calibration** (`vl01TiVTuoQ`, `usho6UVLqkE`) — useful
because "a big order" means different things per market: ES showed a 325 and a
676-contract order; DAX prints `1,1,2,4,3,5,33` and `2,4,8,11,7`; bond futures
carry 5,000–6,000 a side; gold shows 2, 4, 6.

## Where this channel contradicts the rest of the corpus

**1. Heatmaps — a genuine methodological dispute.** Carmine's ep. 3 makes the
**Bookmap heatmap** a core instrument. `Vd83oo_geMk` (00:58) states that
institutions and his own group **do not rely on heatmaps**, and that the order
book is the true market (01:07): a heatmap shows where limit orders sit or
*sat*, but not execution speed and not intent. Two order-flow practitioners,
same object, opposite conclusions about whether the visualisation adds
information or launders it. Neither offers statistics; the corpus cannot
adjudicate.

**2. It rejects the ICT / liquidity-sweep school outright.** This is the
sharpest cross-corpus finding of the sweep, and it is stated three times
independently:

- Stop-hunting is *"a retail trading myth"*, with evidence: footprints show
  **single-digit** contract trades printing below chart lows, so there is no
  institutional size down there doing the hunting (`RwQBdF9TSvc` 02:30, 02:53).
- ICT narratives that banks sweep stops for liquidity are *"hyped up and
  inaccurate"* (`RwQBdF9TSvc` 04:23).
- The retail "stop-loss waves" concept is dismissed, with rapid moves
  attributed instead to **institutional futures hedging** (`aursfDVYzUk` 09:51).

This contradicts the entire method of [`IUWvHVout94`](../videos/IUWvHVout94/CARD.md)
(Trading Notes: identify pool → wait for sweep → enter on confirmation) and the
sweep-then-ChoCH architecture of the Smart Money Decode X series.

It is, however, a **partial agreement** with Trading Notes on the thesis
itself: that video's own on-screen claim is `"NOBODY IS HUNTING YOUR STOPS"`
(00:30). Both sources reject malice; they diverge on whether the mechanical
effect is large enough to trade. Trading Notes builds a strategy on it; this
channel says it is largely not there.

**3. Support and resistance as fixed price points "do not truly exist"**
(`RwQBdF9TSvc` 19:50) — against Carmine ep. 5, which is entirely about
validating S/R with order flow.

**4. Internal contradiction on entry.** `NkQeOVDTAec` teaches **pullback after
breakout**; `zAwEX_tRUfE` teaches entry **on the break**. Same presenter, no
published rule for choosing. This was originally logged as a Vorwald-versus-
Carmine conflict and has been corrected on both cards — it is internal.

## Where it converges with the corpus (independent arrivals)

These matter because the sources do not cite each other:

- **Absorption / trapped participants** — `usho6UVLqkE` 14:24 vs Carmine ep. 2/5.
- **Volume tails** — his buying/selling tails (`K8qtT2_axPo` 13:21) are
  Carmine's "volume tail": prints thinning at an extreme.
- **Iceberg orders** — `Vd83oo_geMk` 14:10, Carmine ep. 2, and Trading Notes
  `IUWvHVout94` 04:57. Three independent arrivals.
- **Auction premise / balance and imbalance** — the whole sweep, Carmine ep. 1,
  and SMDX.
- **Break-and-retest** — `NkQeOVDTAec` 05:38 vs Carmine ep. 3/6.

## What is NOT specified anywhere in the sweep

- **What `PbD` stands for.** It is used as a named model in `NkQeOVDTAec`
  (00:08) and `0CrkbfuIhkc` (03:10) and expanded in neither; `usho6UVLqkE`
  never mentions it at all. **The four PbD videos are all in the blocked set.**
- **A delta threshold.** Delta is visible on his footprint (`Vd83oo_geMk`
  08:16) but no numeric trigger is given — the same gap Carmine has.
- **Position sizing.** No contract counts, no account risk percentage.
- **Exit rules** beyond "target the opposing level" and R:R > 2.
- **Any executed trade.** Across all ten videos there is **no live execution,
  no fill, no P&L and no broker connection** — only annotated illustrations.
  The `yWO8hVpRXeY` LIVE DAY TRADING video is in the blocked set and is the
  natural test of whether this channel ever shows a real trade.
- **Costs.** No commission, spread or slippage anywhere.

## Open items

1. **Expand `PbD`** — run `Ly62G168MkQ`, `jXR1afMy-3o` or `m3IMdc7QwN4`.
2. **Grade the "80–90% Win Rate" claim** (`uFxYcpiaOpw`) with the win-rate/R:R
   identity. At an 80% hit rate the break-even R:R is only 0.25, so the claim
   is survivable in principle — the question is what R:R he pairs it with.
3. **Verify the championship claims.** `2022-2023 Patrick Nill 219.1% Global
   Cup Championship of Forex Trading™` and `2024 Quarterly Futures Day Trading
   Championship Q2 2nd Christoph Radecker 97.70%` (`NkQeOVDTAec` 00:36–00:40),
   against `2 Patrick Nill 202.1%` / `3 Christoph Radecker 47.7%`
   (`0CrkbfuIhkc` 00:28–00:32). **The figures differ between videos** and none
   is verified against the World Cup Trading Championships public record.
4. **Resolve the presenter's name.** The speaker self-identifies as *"Thomas
   Voigt, coach and trainer of Patrick Nill"* (`aursfDVYzUk` 00:19) while
   another pass renders the same voice as *"Thomas Vorwald"* (`0CrkbfuIhkc`),
   and the handle is `@tom_vorwald_en`. Unresolved; do not assert a legal name
   from this corpus.
5. **Why he treats POC unconventionally** (`YmygDgtoxO8` 06:55) — stated,
   never explained. Zoom 06:40–07:30.
6. **Score the dated outlook** in `0CrkbfuIhkc` (ES below 6,850 → 6,300 →
   4,600; BTC acceptance below 72,000; AAPL below 240; GOOGL above 325 on a
   close; TSLA below 400) against what the market subsequently did — the same
   treatment the Trade Brigade newsletter gets.

## Coverage and what is missing

The sweep stopped at 10 of 19 because the Gemini key hit
`GenerateRequestsPerDayPerProjectPerModel-FreeTier`, **limit 20 requests per
day per model**. The completed 10 are the entire order-flow and profile core.
The 9 blocked are the **PbD cluster (5, including the only LIVE trading
video), VWAP (2), a volume-trading video and the 80–90% win-rate claim** —
i.e. exactly the videos that would settle what PbD means and whether this
channel ever demonstrates a real trade.

Consumed: **915,466 Gemini prompt tokens** across the 10 completed passes.
