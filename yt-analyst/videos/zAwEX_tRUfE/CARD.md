# Video: zAwEX_tRUfE

- **URL:** https://www.youtube.com/watch?v=zAwEX_tRUfE
- **Title:** My Simple 1-Minute Scalping Strategy for $10,000/Month
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-09-04 · **Duration:** 10:38 (638 s)
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-br7 (graded through the orderflow / volume-at-price lens)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**Framing.** German-language, AI-dubbed to English (stated in the description).
Agenda cards at 00:28–00:38: `Why scalpers lose` · `What you need` ·
`The Entry technique` · `My complete Setup`. End card `Trade The Traders`
(10:18). Instrument and platform are on screen at 00:50:
`#ES[M] Continuous[c] | Powered by dxFeed`. **ATAS** is the platform;
**dxFeed** is the market-data vendor behind it, not something you look at.
`#ES` is ATAS's symbol notation for the E-mini S&P and `Continuous[c]` a
back-adjusted rolled series, so the chart runs unbroken across quarterly
rolls rather than showing a single expiry. 1-minute chart, with a
Market-Profile/TPO + volume-profile pane split against the candles (01:40).

**The thesis.** Scalpers lose not from bad signals but from bad *location*:
trading "in the middle of a price zone that mathematically offers zero edge"
(description). Context comes from the **prior day's Value Area**, computed
once; the 1-minute chart then carries **no indicators at all**.

**The two trades he contrasts.**

*The bad trade (04:20–05:10) — inside value.* Retail buys inside the prior
day's value area and "take[s] the risk below the last low" (04:30), targeting
the upper boundary. He estimates the resulting **risk-reward at ~0.8** (04:42)
and concludes, verbatim: *"you need a win rate of at least a good 60% to even
be at break even with many, many trades"* (04:48).

*The good trade (06:50–09:40) — expansion out of value.* Entry is the break
above the **prior-day Value Area High**, labelled on his chart in German
`Value Area High Vortag` (05:46, 06:51). His words: *"if it breaks above this
point then I am officially leaving the previous equilibrium area"* (08:44).
Stop is invalidation by acceptance back inside: *"you're out relatively
quickly down here if the market accepts the old equilibrium again"* (07:33).
Target is the expansion run. He writes `CRV` (09:28) — *Chance-Risiko-
Verhältnis*, risk-reward — and concludes: *"So even with just a 50 or 60% win
rate, you can make money with this"* (08:06).

Supporting context, spoken: a **single print** area on the profile where he
expects strength (02:08); equilibrium/target at **7485** (02:47, 03:10, drawn
as an orange line in MS Paint); an example entry near **7482** (01:17); and an
"accumulation" forming just below the equilibrium line (06:14). He names a
`PbD` setup (01:00, and in the description) but **never says what the letters
stand for** — flagged by Gemini's uncertainties and unresolved.

### Arithmetic check on the load-bearing claim

His whole argument is a win-rate/R:R identity, so it is checkable:

| R:R | Break-even win rate |
|---|---|
| 0.8 | **55.56%** |
| 1.0 | 50.00% |
| 1.5 | 40.00% |
| 2.0 | 33.33% |

- **Claim 1 is conservative, not wrong.** At R:R 0.8 the gross break-even is
  **55.56%**, not "a good 60%". He overstates the requirement by ~4.4 points.
  Given ES friction that is a defensible practical rounding, not an error —
  but it is a rounding, and he presents it as the arithmetic.
- **Claim 2 is unfalsifiable as stated.** "Profitable at 50–60%" is only true
  above a threshold R:R: 50% needs **R:R ≥ 1.00**, 60% needs **R:R ≥ 0.67**.
  **He never gives the expansion trade's R:R** — no point distance for the
  stop, none for the target, no CRV number (confirmed by a dedicated zoom,
  runs/20260906-034104). So the recommended setup is the one he does not
  quantify.
- **The argument is asymmetric.** He is numerically rigorous where he
  *condemns* (the 0.8 mid-range trade) and purely qualitative where he
  *recommends*. That asymmetry is the video's central weakness.

**Cost note from our own ES tick work** (see [UL5QOCSKnU0](../UL5QOCSKnU0/CARD.md)):
at $17 round turn per contract, a 2-point scalp stop costs **0.17 R** in
friction — about a third of the edge at 60% WR / R:R 2.0. Vorwald never
mentions costs, and on a 1-minute timeframe they are not a rounding error.

**No trade is shown.** The teaching is done on a static screenshot pasted into
**MS Paint** and annotated by hand (03:06 onward). No fills, no order panel,
no P&L, no replay. This is an illustration and is not presented otherwise —
honest, but it means nothing here is evidence.

**No pitch inside the video.** The description links `worldclassedge.com`
("Learn from World Class Traders for FREE") and the WorldClassEdge socials;
the video itself sells nothing and states no price. Notably clean against the
rest of this corpus — no affiliate links at all, in contrast to
[Trading Notes](../IUWvHVout94/CARD.md) and [AlgoTrade Pro](../UL5QOCSKnU0/CARD.md),
which share the same Flux Charts sponsor.

## Graded against the orderflow corpus

Baseline: [`playlists/orderflow-series-…`](../../playlists/orderflow-series-PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ.md)
(Carmine Rosato, 8 episodes).

**Steve's read is correct: this is order flow without the word.** The video
never says "order flow", "delta" or "absorption", but every load-bearing
element is volume-at-price:

- **Same auction premise.** Vorwald's "equilibrium area" and "leaving the
  previous equilibrium" is Carmine ep. 1 verbatim in substance: balance = a
  range where buyers and sellers agree; an event creates imbalance → new
  range. Neither man cites the other; they are describing one theory.
- **Trade location derived from where volume actually traded.** The prior-day
  Value Area *is* a volume-at-price object. This is Carmine's ep. 6 volume
  frameworks with the measurement moved from the live tape to yesterday's
  close.
- **"Accumulation" below the equilibrium line** (06:14) is absorption in
  Carmine's vocabulary — passive interest building against the prevailing
  push.
- **Both reject indicators on principle.** Vorwald: no indicator on the chart.
  Carmine: indicators are downstream of order flow.
- **He is running an order-flow-native platform and using almost none of it.**
  ATAS exists for footprint/cluster charts, cumulative delta, DOM and tape —
  the exact instruments Carmine's whole method is built on, and the same
  category of tool as Sierra Chart and Bookmap elsewhere in the corpus.
  Vorwald pays for all of it, uses the market profile and volume profile to
  fix context **once**, and then trades a bare 1-minute candlestick chart.
  This is the strongest evidence that the missing vocabulary is deliberate
  style rather than a gap in the method: he is not unaware of order flow
  tooling, he is choosing its cheapest layer. It also makes the "accessible
  branch" reading concrete — same platform as the professionals, a fraction
  of the cognitive load.

**Where it departs from the corpus.** Carmine's ep. 3/6 rule is explicit:
*never buy the initial break — let it break, buy the pullback; a defended
retest proves the participants*. And his default posture is reversion:
*~99% of the time look for the reversal on the first test*. **Vorwald's
recommended entry here is the initial break itself**, with no retest and no
pullback requirement.

**AMENDED 2026-09-06 (bead dr-cle).** This was first recorded as the corpus's
sharpest *cross-source* conflict — Vorwald versus Carmine. That reading was
wrong, and [HySZZSjMxF8](../HySZZSjMxF8/CARD.md) overturned it. In that video
Vorwald teaches the **reversion** trade: a counter-trade at a pre-located
level gated on volume-exhaustion confirmation, plus a failed breakout entered
on **re-acceptance** — which is Carmine's "buy the pullback" in other words.

So Vorwald runs **both** postures: expansion out of value on the 1-minute
chart, reversion at a level on the 15-minute. The conflict is not between
sources; it is **internal to Vorwald**.

**FURTHER AMENDED 2026-09-06 (epic dr-zk8) — the switching rule does exist.**
The channel sweep found it in the VWAP video
([43JaKHRvxHk](../43JaKHRvxHk/CARD.md)): **classify the market's structure
first, then choose the mode.** In an established trend, the tool is a
**pull-back entry** (continuation); when structure is horizontal and balanced,
it is a **mean-reversion target** (03:22, 04:50, 06:30). The same rule is
restated independently in [VumVuGnCcFM](../VumVuGnCcFM/CARD.md) (10:35):
mean-reversion only when structure is sideways and balanced. The underlying
regime split is his 70/30 — balance about 70% of the time, imbalance about
30%, attested in six separate videos.

The criticism that survives is that **neither of the two entry videos states
the switching rule**, so a viewer who watches only the scalping video receives
an expansion method with no indication that it is the minority regime — the
30% case, by his own numbers. Treat any single Vorwald video as one mode of a
system whose selection rule is published somewhere else on the channel.

Secondary divergence: Carmine confirms in **"The Now"** — live tape or
footprint, *never a candle close*, because waiting for a close widens the stop
from ~2 pts to ~7 pts and kills the R. Vorwald requires no confirmation at all
beyond the break, and his stop is not a point distance but an *acceptance*
condition ("if the market accepts the old equilibrium again"). Acceptance is a
slower, looser trigger than anything Carmine would accept, and it is
unquantified here.

## What is unique — the extractable aspects

1. **He supplies the number the entire orderflow series omits.** The synthesis
   lists under *"What is NOT specified anywhere in the series"*: no delta
   threshold, no position sizing, no exit rules, **and no win rate**. Vorwald
   makes win rate the centrepiece and binds it to R:R by identity. Even at his
   level of rigour this is the corpus's only stated relationship between hit
   rate and trade location.
2. **Location quality expressed as arithmetic rather than intuition.**
   Carmine asserts that location matters and demonstrates it with winners.
   Vorwald *derives* it: bad location → R:R 0.8 → you need ~56–60% just to
   tread water. That derivation is portable to any setup we grade, and it is
   now the cheapest first test to run on any new strategy video.
3. **A no-live-tape operating model, on order-flow-native software.**
   Carmine's method needs Sierra Chart, footprint, DOM and Bookmap. Vorwald
   computes context **once** from the prior session's profile and then trades
   a bare 1-minute chart — on ATAS, which offers him every one of Carmine's
   instruments and which he declines to use. Same theory, same class of
   platform, an order of magnitude less cognitive load. The accessible
   branch, and the only one in the corpus reachable without reading a live
   tape.
4. **The mid-range trade named as a mathematical error.** "Somewhere in the
   middle of a price zone that mathematically offers zero edge" is a claim no
   other video in the corpus makes explicitly, and it is the natural inverse
   of Carmine's edge cases.
5. **Expansion as the primary trade.** Every other volume-based source we hold
   is reversion-first. This is the corpus's only expansion-first framework.
6. **ATAS + dxFeed** — new platform for the corpus (we hold Sierra Chart,
   ThinkorSwim, TradingView, Bookmap).

## Grade

**Clarity: B.** The concepts are clean, the context method is genuinely fast,
and the R:R-to-win-rate argument is the most useful minute in the video. It
loses a grade for the asymmetry: the rejected trade gets numbers, the
recommended trade gets none — no stop distance, no target distance, no CRV,
no cost. `PbD` is used and never expanded. And an entry defined as "it breaks
above this point" is not precise enough for two traders to fill at the same
price on a 1-minute chart.

**Alignment to the orderflow corpus: A.** Higher than its clarity. It is the
same auction theory, the same volume-at-price logic and the same rejection of
indicators, arrived at independently and expressed in different vocabulary —
which is exactly what makes it useful. It converges with Carmine on premise
and diverges on execution in a way we can state precisely.

**Net.** Worth keeping and worth mining. Take the win-rate/R:R identity as a
standing test for the whole corpus; treat the break-vs-pullback question as
an open item **within Vorwald's own system** rather than against Carmine (see
the amendment above); discount the specific trade, which is undocumented and
unpriced.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — grade through the orderflow/volume lens, extract what is
  unique (bead dr-br7).** Wide pass plus two zooms (the R:R arithmetic,
  runs/20260906-033436; the expansion setup, runs/20260906-034104). Confirmed
  Steve's read that this is order-flow reasoning without the vocabulary.
  Arithmetic showed his 0.8 → "60%" break-even is conservative by 4.4 points
  (true 55.56%) and that his headline 50–60% claim is unfalsifiable because the
  recommended setup's R:R is never given. Verdict: clarity B, orderflow
  alignment A. Sharpest finding: his entry on the initial break directly
  contradicts Carmine's "never buy the initial break — buy the pullback".
  A first zoom attempt hit 429s and was rerun on gemini-3.6-flash.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **German original, AI-dubbed to English.** On-screen writing stays German —
  `Value Area High Vortag` (= prior day), `CRV` (= *Chance-Risiko-Verhältnis*,
  risk-reward ratio). Ask Gemini to transcribe German verbatim *then*
  translate, or the labels come back paraphrased into English and the actual
  on-screen text is lost.
- **He teaches in MS Paint** over a static chart screenshot. There is no live
  platform state to read, so frames buy nothing beyond what a zoom gives —
  grade this channel with arithmetic and verbatim quotes instead.
- Platform is **ATAS** ("Advanced Time And Sales") on a **dxFeed** data feed,
  ES continuous (back-adjusted, rolled); the profile pane and the 1-minute
  chart are split side by side (01:40). ATAS is an order-flow platform —
  footprint, delta, DOM — so when grading this channel, note *which* of its
  features are on screen. Vorwald uses only the profile side, and that
  restraint is itself a finding.
- The channel brands as "Trade The Traders" on the end card while the handle
  is `@tom_vorwald_en` and the description points to WorldClassEdge — three
  names for one source. Index under **Tom Vorwald EN** so the grouping holds.
- No affiliate links anywhere, which is rare in this corpus.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-033158 [00:00-00:20] gemini-3.6-flash (tok 2061/96) — Q: In one sentence, what is on screen at the start of this video? — runs/20260906-033158/
- 20260906-033315 [full] gemini-flash-latest (tok 58677/1746) — Q: Map this video end to end for an analyst studying ORDER FLOW and VOLUME-BASED tr… — runs/20260906-033315/
- 20260906-033436 [04:20-05:10] gemini-3.6-flash (tok 4993/455) — Q: This window contains the presenter's risk-reward arithmetic — the load-bearing c… — runs/20260906-033436/
- 20260906-033609 [06:50-09:40] gemini-3.6-flash (tok 15994/1031) — Q: This window contains the video's actual RECOMMENDED setup — the expansion trade … — runs/20260906-033609/
- 20260906-033619 [06:50-09:40] gemini-3.6-flash (tok 15923/643) — Q: Transcribe the video's RECOMMENDED setup — the expansion trade above the prior-d… — runs/20260906-033619/
