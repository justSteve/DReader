# Video: VumVuGnCcFM

- **URL:** https://www.youtube.com/watch?v=VumVuGnCcFM
- **Title:** The ONLY VWAP-Video you will EVER need
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Duration:** 11:59
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

Companion to [43JaKHRvxHk](../43JaKHRvxHk/CARD.md) and consistent with it —
useful corroboration, since the two were analysed independently.

**Definition** (00:58): VWAP as a volume-weighted moving average computed on
time and volume, giving the average transaction price over a session; it
**resets to zero when a new trading day begins** (02:05). **VPOC** = the price
with the highest traded volume (02:35); **VAH/VAL** as the boundaries around
that node (02:41). **Equilibrium** (04:05) = the balanced state in which large
institutional participants **build up and unwind** positions — the clearest
statement of *why* the value area matters that the corpus holds.

**The numbers:**
- The market reverts to equilibrium/VPOC roughly **70%** of the time (09:02).
- Strong trend days written on the canvas as **>20%** (09:48). Note this is a
  *third* figure alongside the channel's usual 30% imbalance share — 70/30 and
  70/>20 do not quite reconcile, and he does not address the gap.

**The rule** (10:35): trade mean-reversion bounces to VWAP **only when market
structure is sideways and balanced**. Identical in substance to
[43JaKHRvxHk](../43JaKHRvxHk/CARD.md)'s Rule 1, arrived at in a different video.

**The risk warning is the most honest sentence on the channel** (11:07): a
trader may succeed **20 times** adding counter-trend to VWAP and be
**liquidated on the 21st** during a runaway trend. That is a plain statement of
negative skew — a high hit rate concealing a fat left tail — and it is the
implicit counter-argument to his own
[80–90% win-rate video](../uFxYcpiaOpw/CARD.md).

**Single prints** indicate aggressive participants driving directional
continuation, invalidating mean-reversion plays (07:30).

**A third variant of the presenter's name.** At 00:29 the speaker is
transcribed as introducing himself as **"Tom Freiwald"**, referencing a trader
**"Patrick Nohr"** — against "Thomas Voigt"/"Patrick Nill"
([aursfDVYzUk](../aursfDVYzUk/CARD.md)) and "Thomas Vorwald"
([0CrkbfuIhkc](../0CrkbfuIhkc/CARD.md)). Three renderings of one German surname
across three passes. **This settles that the variation is Gemini
transcription noise, not multiple presenters** — and it confirms that no name
should be asserted from audio in this corpus.

Chart: `Inside Dax Future 60 min (08:00:00 - 22:00:00) Eurex` (01:25) with
session VWAP, volume histogram and a right-axis volume profile.

**No trade, no stop/target, no R:R, no win rate.**

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: corroborates the VWAP regime rule independently; states the negative-skew warning (20 wins then liquidation) that undercuts the channel's own 80-90% win-rate video. Third name variant settles the transcription-noise question.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Name variants across the sweep are transcription noise**: Vorwald / Voigt /
  Freiwald, Nill / Nohr. Never assert a personal name from Gemini audio here.
- The `>20%` trend-day figure does not reconcile with the channel's usual 30%
  imbalance share; note the discrepancy rather than averaging it.
- The 11:07 negative-skew warning is the best argument against his own
  high-win-rate framing — cross-reference the two.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101652 [full] gemini-flash-latest (tok 66101/1053) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101652/
