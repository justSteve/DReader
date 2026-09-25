# Video: uFxYcpiaOpw

- **URL:** https://www.youtube.com/watch?v=uFxYcpiaOpw
- **Title:** My Simplest Trading Strategy (80–90% Win Rate)
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-07-22 · **Duration:** 9:33 · **Views:** 12,268
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**The claim.** A hit rate of **80% to 90%** (00:02), for a setup that occurs
**"Once a day"** on screen (00:06); spoken it is *"about once a day"* and works in only **30%** of market phases
(00:18, pie chart) — the imbalance share of his 70/30 split.

**The setup, in order:** weekly/daily volume **balance versus imbalance** →
locate **daily rising VPOCs** (defined at 02:16 as the price levels where the
market had the most volume) → wait for an **open outside balance** → drop to the
**1-minute** chart (06:28) → confirm a **`P` profile**, i.e. aggressive buyers
shifting balance upward (06:41) → **enter on a candle CLOSE above the
consolidation level, not a wick trade-through** (07:15, explicit).

**Idea and Proof, in the original German** (07:31, 07:44):
> `IDEE: das der Markt schnell wird` — "IDEA: that the market becomes fast"
> `BEWEIS durch ein Break Out Setup` — "PROOF through a breakout setup"

This confirms the Idea/Proof framework named in
[NkQeOVDTAec](../NkQeOVDTAec/CARD.md) and shows the Idea is a *hypothesis about
speed*, not merely a price level.

### The claim, checked

**Stop distance, target, tick measurements and risk-reward are all ABSENT**
(explicit in the pass). That is fatal to the headline, because win rate alone
decides nothing. Applying the identity used throughout this corpus,
break-even R:R = (1 − p)/p:

| Claimed hit rate | Break-even R:R | Verdict |
|---|---|---|
| 80% | **0.25** | survivable — a low bar |
| 90% | **0.111** | survivable — a very low bar |

So the claim is *not implausible*: high-hit-rate systems are normally
small-R systems, and at 80% you only need to make a quarter of what you risk.
**But he never states the R:R, so the claim cannot be evaluated** — and the
direction of the omission matters, because the only number that could falsify
it is the one missing.

**It also sits awkwardly against his own framework.**
[NkQeOVDTAec](../NkQeOVDTAec/CARD.md) works an example at a **50% hit rate
giving an average risk-reward of "maybe a two"**;
this video claims **80–90%**. Both can be true of different setups, but the
channel never reconciles them, and a viewer taking both at face value would
have no idea which regime they are trading.

**Cost note.** At a 1-minute entry the stop is small, and our own ES tick work
([UL5QOCSKnU0](../UL5QOCSKnU0/CARD.md)) puts friction at 0.17 R on a 2-point
stop. Against a break-even R:R of 0.25, friction of that order is not a
rounding error — it is most of the margin.

Platform reported as **ATAS** inside MS Paint (01:05) — a `verbatim: null` visual claim, absent from the transcript and frame-unverified; weekly profile left, daily profiles
right (01:15). Instrument: he says only *"the Nikkei future"* (03:31). **ES** and **225 mini** come from a chart title Gemini's own uncertainties call *"tiny and partially compressed"* — treat as unread. `PbD`
referenced at 00:24, **not expanded**. Leaderboard `Patrick Nill 202.1%` (00:27).

**No live execution, no fills, no brackets, no P&L** (08:35).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: the 80-90% claim is survivable in principle (break-even R:R only 0.25) but unfalsifiable as given -- stop, target and R:R are all absent, and it is unreconciled with the channel's own worked example at a 50% hit rate and an average risk-reward around two.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **The headline number is the one that cannot fail; the missing number is the
  one that could.** Whenever this channel leads with a win rate, look for the
  R:R — it is absent here, and in [NkQeOVDTAec](../NkQeOVDTAec/CARD.md) it is only *"maybe a two"* inside a worked example. *(This bullet still carried the old ">2" phrasing after the rest of the card was corrected — fixed 2026-09-06.)*
- Entry requires a candle **close** above consolidation (07:15) — third
  attestation of the channel's close rule.
- The Idea is a hypothesis about *speed*, not a level: "IDEE: das der Markt
  schnell wird".


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101517 [full] gemini-flash-latest (tok 52898/1271) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101517/
