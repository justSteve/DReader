# Video: K8qtT2_axPo

- **URL:** https://www.youtube.com/watch?v=K8qtT2_axPo
- **Title:** Market Profile: How Trading World Champions REALLY read the Market!
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-01-07 · **Duration:** 16:25 · **Views:** 25,597
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**Platform: Sierra Chart, on the S&P future.** *(Corrected 2026-09-07 by frames:
`frames-012-040/f_0006.jpg` at 00:22 shows the chart header `ESH26-CME
[CBV][M] #4 - Period: 1 Days, TPOs: 1.25 x 30 min · 2025-12-18`, a price axis
of 6,780–6,960, and no watermark anywhere. "Powered by VolFix.net" was one
run's `verbatim: null` visual claim; the fallback run read "shiftnest".
Screenshots are taken and annotated in **HyperSnap 8** (German UI), not MS
Paint.)*

**The corpus's most complete Market Profile vocabulary.** Attributed at 01:03
to **Peter Steidlmayer**, who developed TPO (Time Price Opportunity).

| Concept | His definition | t |
|---|---|---|
| Market Profile | a **time**-based tool showing momentum and lethargy across standardised **30-minute** blocks | 01:24 |
| vs Volume Profile | volume-based; market profile is time-based | 02:15 |
| Initial balance | the opening 30 minutes / opening range | 02:55 |
| Normal / balanced profile | an oscillating market taking a **bell-curve** shape | 03:29 |
| Buying tail | rapid upward rejection — price spent only 30 minutes before shooting up | 05:18 |
| **POC vs VPOC** | POC = where the market spent the most **time**; explicitly distinguished from **VPOC**, the volume-weighted point of control | 05:34 |
| Value area | where the market spent **70%** of main trading time | 05:45 |
| Normal variation | a balanced profile that rejected price on one side | 08:40 |
| Double distribution | two profiles in one session separated by **single prints** | 11:09 |
| Single prints | individual letters in the profile; high probability of a trend profile | 11:21 |
| Selling / buying tail | single letters at the **top** / **bottom** of the profile | 13:21 |
| Ledgers | multiple letters terminating at one price level — **weak hands** | 13:37 |

**The POC/VPOC distinction is a precision the corpus did not have.** Carmine
and SMDX both use "POC" loosely; separating time-weighted from volume-weighted
control is a real analytical improvement and it matters, because the two
diverge exactly where the interesting trades are (see the "anomaly" in
[1utSjHs_Mq8](../1utSjHs_Mq8/CARD.md)).

**Buying/selling tails are Carmine's "volume tail" by another name** — prints
thinning at an extreme, the last buyer having bought. Independent arrival on
the same signal.

**A frequency claim** (10:41): **70% of the time the market trades in balanced
sideways phases.** Unsourced, but checkable, and it is the corpus's only
stated base rate for market state.

Price axis around `6815.00 / 6835.00 / 6850.00 / 6915.00`, current
`6850.75` (02:25). Instrument not legible — an index future, NQ or DAX/Euro
Stoxx (Gemini declined to guess). Branding `WORLD CLASS EDGE` (16:06).

**No trades, no entries, no tick distances, no P&L** — explicitly context, not
mechanical rules.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** One standardised
  orderflow-focused wide pass, identical question across the sweep for
  comparability. Verdict: the corpus's fullest Market Profile vocabulary, including the POC-vs-VPOC distinction it previously lacked. Context only, no rules.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Sierra Chart** is the platform (frame-verified 2026-09-07: header
  `ESH26-CME [CBV][M]`); the same menu bar appears in `1utSjHs_Mq8`. The
  "VolFix" reading is withdrawn. Instrument here is **ESH26**, the March 2026
  S&P future — the axis Gemini could not read is 6,780–6,960.
- POC (time) vs VPOC (volume) — use this distinction when reading any other
  card's "POC" claim; older corpus cards do not make it.
- Instrument is illegible; do not attribute a symbol to this video.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-072300 [full] gemini-flash-latest (tok 90385/1443) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072300/
- 20260906-072315 [full] gemini-3.6-flash (tok 90385/882) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072315/
