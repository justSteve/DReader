# Video: 43JaKHRvxHk

- **URL:** https://www.youtube.com/watch?v=43JaKHRvxHk
- **Title:** 90% of Traders Use VWAP WRONG! (Here's How to Do It Right)
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-07-03 · **Duration:** 10:41 · **Views:** 7,754
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**The best-argued video in the sweep**, because it makes VWAP's usefulness
conditional on regime and says so plainly. Handwritten German on the opening
chart (00:35): `VWAP... mal klappt es mal nicht!` — *"VWAP… sometimes it works,
sometimes it doesn't!"*

**Definition** (00:58): VWAP is strictly the **volume-weighted average price of
the current day**, and it **resets and recalculates at the start of every
trading day** (01:34). Platform is **Sierra Chart** with German localisation
(01:18); the study bar reads `Euro Total Volume No Days: 0.00 VWAP: 25191.00 -
Volume Weighted Average Price … Varianz: 0.5; 1; 1.5; 2` (01:54) — so he runs
**variance bands at 0.5, 1, 1.5 and 2**, the only VWAP band settings in the
corpus.

**The regime rule — the actual content:**
- Markets trend stably only **~30%** of the time and are non-trending **~70%**
  (02:18). Sixth attestation of the split.
- Using VWAP blindly as a **counter-trend** tool across all regimes produces
  **excessive stop-outs** (03:15).
- **Rule 1** (03:22): VWAP **pull-back** trading requires an established
  **trend** context.
- Classify the **market open structure first** to decide whether continuation is
  viable (04:50).
- When VWAP is **horizontal**, treat the market as balanced and **range-scalp
  toward VWAP** rather than expecting breakouts (06:30).

So: trending → VWAP is a dynamic **pull-back entry**; balanced → VWAP is a
**mean-reversion target**. Same tool, opposite use, selected by regime. **This
is the clearest statement of regime-dependence anywhere in the corpus**, and it
is the missing piece for the mode-switching problem logged against
[zAwEX_tRUfE](../zAwEX_tRUfE/CARD.md): the channel *does* have a selection
rule, and it is "classify the structure first".

Channel identity on screen (00:34): `Tom Vorwald EN / 42.8K subscribers`.
`PbD` is **not mentioned anywhere** in this video (explicit).

**No trade, no stop/target distances, no R:R, no win rate.**

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: the clearest regime-dependence argument in the corpus -- VWAP as pull-back entry in trend, mean-reversion target in balance, selected by classifying structure first. Supplies the mode-switching rule the scalping card said was missing.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Cite this for the channel's mode-switching rule**: classify structure
  first, then choose continuation or reversion. It partly answers the
  expansion-vs-reversion contradiction logged on zAwEX_tRUfE.
- His VWAP variance bands are **0.5, 1, 1.5, 2** — the corpus's only VWAP
  parameterisation.
- Sierra Chart with German localisation; subscriber count 42.8K at analysis.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101633 [full] gemini-flash-latest (tok 59001/1102) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101633/
