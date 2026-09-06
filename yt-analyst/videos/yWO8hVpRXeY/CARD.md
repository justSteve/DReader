# Video: yWO8hVpRXeY

- **URL:** https://www.youtube.com/watch?v=yWO8hVpRXeY
- **Title:** LIVE DAY TRADING — How I Apply the PbD Strategy on the DAX Future!
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Duration:** 17:56
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**This is the only executed trade in the entire sweep, and it corrects the
sweep's earlier finding that the channel never shows one.**

**Real execution, not illustration.** The **ATAS DOM Trader execution panel** is
on screen at 15:52 with German controls — `Schließen`, `Kauf MKT`, `Verk MKT`,
`Standardwert` (close / buy market / sell market / default). A six-panel ATAS
workspace runs candlestick charts, **DOM ladders**, volume profiles and
**cluster/footprint** charts (01:00).

**The trade, with numbers:**

| Element | Value | t |
|---|---|---|
| Plan | short below **112**, into the Asian-session lows | 01:09 |
| Stop rule | **above market structure**, explicitly *not* arbitrarily moved to breakeven | 03:49 |
| Initial R:R | **1:2** | 04:55 |
| Risk | **23 ticks**, R:R revised to ~**1:3** | 09:56 |
| Result | **74 ticks** locked in by trailing the stop above the local balance area | 14:03 |

**Arithmetic check:** 74 ticks realised against 23 ticks risked = **3.22 R**,
which closes against the stated ~1:3 target. The figures are a coherent set.
This is the only place in the sweep where a stated risk, a stated target and a
realised outcome all appear together and reconcile.

**Note what the stop rule rules out.** "Above market structure rather than
arbitrarily moved to breakeven" is a direct rejection of the
move-to-breakeven-at-1R habit that the AlgoTrade Pro backtest
([UL5QOCSKnU0](../UL5QOCSKnU0/CARD.md)) hard-codes into its exit. Two sources in
this corpus, opposite advice on the same decision.

**A genuinely novel input: Euwax Sentiment** (11:53, 12:05) — the Stuttgart
Stock Exchange's retail sentiment gauge, used as a **contrarian** indicator:
extreme positive retail sentiment often precedes declines. **No other source in
the corpus uses a retail-positioning gauge.** It is also the only non-price,
non-volume input anywhere in this channel's method.

**PbD is topic one** (00:07, `PbD concept`) and again **used without expansion**
(00:15); topics three and four are `Order books` and `Footprint charts` (00:27).
**Single prints** indicate aggressive selling during the down move (02:35);
the **VPOC** below price is noted as having been tested yesterday (02:39).

Instruments: DAX futures primarily, plus crude oil and S&P 500. Pitch banner
with QR code at 09:03.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: the sweep's ONLY executed trade -- ATAS DOM Trader panel, 23 ticks risked, 74 ticks realised, 3.22R, arithmetic closes. Introduces Euwax retail sentiment as a contrarian input, unique in the corpus.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **The one live trade on this channel.** Cite it whenever the "no executed
  trade" criticism is raised against Vorwald — it is no longer true, though it
  remains true of the other 18 videos.
- **Euwax Sentiment** (Stuttgart exchange retail gauge, contrarian) is unique in
  the corpus and is his only non-price/volume input.
- His stop rule explicitly rejects moving to breakeven — opposite to the
  AlgoTrade Pro backtest's hard-coded 1R-then-breakeven exit.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101549 [full] gemini-flash-latest (tok 98662/1176) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101549/
