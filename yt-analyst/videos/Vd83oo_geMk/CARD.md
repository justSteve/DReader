# Video: Vd83oo_geMk

- **URL:** https://www.youtube.com/watch?v=Vd83oo_geMk
- **Title:** THE TRUTH about Heatmap & Liquidity — This is how the World Champion REALLY trades!
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2025-11-07 · **Duration:** 15:13 · **Views:** 31,793
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**This video directly contradicts Carmine, and it is the sharpest genuine
cross-source conflict in the corpus.**

Carmine's ep. 3 builds a core tool out of the **Bookmap heatmap** — bands as
resting liquidity, bubbles as executed aggression. Vorwald states at 00:58
that institutional traders and his own group *"Trade the Traders"* **do not
rely on heatmaps**, and at 01:07 that the **order book is the true market**.
His argument: a heatmap shows where limit orders sit or *sat*, but not
execution speed and not intent; the DOM and the footprint show what is
actually being done.

Both men are reading resting liquidity. They disagree on whether the
*visualisation* adds information or launders it. Neither offers statistics,
so the corpus cannot adjudicate — but this is a real methodological dispute
between two order-flow practitioners, not a vocabulary difference.

**He supplies the numeric threshold the orderflow corpus explicitly lacks.**
At 02:44: for ES, an order must be **over 250–300 contracts** — *"or 400, 500,
600"* — to count as truly large. The Carmine synthesis records under *"What is
NOT specified anywhere in the series"*: **no numeric delta or volume
threshold**. This is the first concrete size threshold in the corpus.

**Spoofing** (01:37): placing orders and pulling them right before price
arrives, stated to be **illegal**. Note he is firmer here than in
[vl01TiVTuoQ](../vl01TiVTuoQ/CARD.md), where spoofing is "probably still"
around — a mild internal inconsistency in tone, not substance.

**Iceberg orders** (14:10): a large order continuously absorbed and refilled
at a level without price moving much. Matches the definition in
[IUWvHVout94](../IUWvHVout94/CARD.md) (Trading Notes, 04:57) — third
independent arrival on this concept across the corpus.

**Workspace** (05:38): candles + volume profile, TPO/market profile,
footprint/cluster charts and DOM windows in one layout; a DOM array across
`ZM, CL, Russell, Nasdaq, S&P 500, FDAX` (03:53). DOM shows 20 levels by
default, settable to 100 (04:30, 06:08). Footprint with a delta histogram
along the bottom at 08:16 — so **delta is on his screen**, even though he
does not teach a delta threshold.

**Scaling-in scenario** (10:50): positions 1, 2 and 3 added across ranges
before a crash produces heavy drawdown — offered as a caution.

**No trade, no rules, no R:R, no win rate.** Chart annotation again in MS Paint (09:52).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** One standardised
  orderflow-focused wide pass, identical question across all 19 sweep videos
  for comparability. Verdict: the corpus's sharpest cross-source conflict (heatmaps rejected vs Carmine's Bookmap core), plus the first numeric size threshold (ES > 250-300 contracts).

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Cite this card whenever heatmap/Bookmap evidence is weighed.** Two
  order-flow practitioners disagree on whether the heatmap adds information.
- The ES "truly large" threshold (>250–300 contracts) is the corpus's first
  concrete size number — reuse it when grading claims about big orders.
- Delta is visible on his footprint (08:16) but he teaches no delta threshold,
  same gap as Carmine.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-072108 [full] gemini-3.6-flash (tok 83832/1071) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072108/
