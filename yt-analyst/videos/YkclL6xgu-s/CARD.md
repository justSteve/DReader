# Video: YkclL6xgu-s

- **URL:** https://www.youtube.com/watch?v=YkclL6xgu-s
- **Title:** How powerful is Volume Trading REALLY? World Trading Champion reveals the TRUTH
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2025-12-04 · **Duration:** 13:00 · **Views:** 11,514
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**The most operationally concrete video in the sweep** — it gives a volume
*baseline* method, session timing, and actual stop and target rules.

**A comparative volume baseline, with one number** (02:32, 02:43): roughly **600
contracts** traded in the first 5 minutes after the open. The comparators are
hypothetical — *"just imagine the day before at the market opening, 800
contracts. The day before that, maybe you even had 1,000 contracts"* (02:40–02:50).
*(Corrected 2026-09-07: this card previously recorded 800 and 1,000 as observed
prior-session baselines.)* The method — compare the same window on prior
sessions rather than judge by eye — is real; the figures are an illustration. It is exactly the
threshold discipline that
[HySZZSjMxF8](../HySZZSjMxF8/CARD.md)'s volume exhaustion lacks.

**The delta histogram** (02:18): the bottom histogram is recorded **in delta**
to distinguish buy from sell dominance. So delta *is* used on this channel —
which sharpens the criticism logged on
[Vd83oo_geMk](../Vd83oo_geMk/CARD.md) that he shows delta but teaches no
threshold: here he at least reads direction from it.

**Session structure — the DAX closing auction** (03:32): **17:30–17:35** for the
cash market. The worked institutional example at 04:08 is the clearest
explanation of auction mechanics in the corpus: an order for **150,000 Adidas
shares** with **80,000** worked during the day and the remainder placed **in the
closing auction**. That is *why* closing-auction volume carries information.

**Rules, actually stated:**
- **Stop**: below the **prior established volume consolidation block** (12:04).
- **Target**: **prior historical high-volume zones** (12:10).
- **Weekly signal** (06:19): a weekly candle **close** below a fair price level
  **on low volume** signals an eventual mean-reversion retest upward. Fourth
  attestation of the channel's close rule.

**POC defined as the volume-weighted centre of gravity** (05:40) — a physical
framing not used elsewhere in the corpus.

**Instruments and headers, fully legible:** `FDAX 12-23 (3 Min) … 2023-11-13`
(01:54), `FDAX12-23 (EUREX) … Period: Weeks, 2023-11-19 | Volume Profiles: U, S`
(05:22), and a footprint at `FDAX03-24 (EUREX) … Period: 60 Min, 2024-01-09`
(08:41). Benchmark set named at 12:26: **ES, FDAX, CL**.

`PbD` is **neither spoken nor displayed** (explicit). A Thunderbird desktop
notification leaks on screen at 10:57 — static screenshots, personal desktop.

**No live trade, no R:R, no win rate.**

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: the sweep's most operationally concrete video -- a comparative volume baseline (600 contracts in the first 5 minutes against hypothetical 800/1,000 — corrected 2026-09-07), DAX closing-auction timing and mechanics, and explicit stop and target rules.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Cite this for the channel's only volume baseline method**: compare the
  first 5 minutes' volume against the same window on prior days. It is the
  threshold discipline the volume-exhaustion video lacks.
- DAX cash closing auction is **17:30–17:35**; the 150,000-Adidas example
  explains why closing-auction volume is informative.
- Chart headers here are fully legible (FDAX 12-23, 03-24, EUREX) — use this
  card when a dated instrument reference is needed for the channel.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101710 [full] gemini-flash-latest (tok 71655/1213) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101710/
