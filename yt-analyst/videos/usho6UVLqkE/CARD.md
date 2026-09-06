# Video: usho6UVLqkE

- **URL:** https://www.youtube.com/watch?v=usho6UVLqkE
- **Title:** World Champion reveals the Orderflow System that 95% of Traders do NOT know!
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2025-11-27 · **Duration:** 17:43 · **Views:** 24,203
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**DOM and footprint, taught from live order books.** DOM defined at 01:50 as
the real-time orders resting on both sides; the slide lists the German column
labels `Informationen / Working Orders / Offer / Preis / Last Trade Volume
Profile / Bids`. Four DOM windows are compared side by side (02:32) across
**Russell, ES and the DAX future**.

**Observed sizes** — again the calibration value:

| Market | Reading | t |
|---|---|---|
| Russell | 3 limit buys at **2247.1** | 02:47 |
| ES | sell blocks of **74** and **48** | 04:01 |
| DAX | `2, 4, 8, 11, 7` | 04:12 |
| ES | a **676**-contract bid | 06:18 |
| Russell profile | volume peak at **2246.4** | 05:03 |
| Footprint | **712** market orders sold at one price in a 5-min block | 12:06 |

**Front-running, defined** (09:19): a large resting buy order acts as a
**magnet** — price is drawn toward it. This is *new to the corpus*. Carmine's
series has absorption and trapped participants, but nothing that treats a
large passive order as an attractor to be traded toward rather than faded.

**Absorption, defined** (14:24): a buyer repeatedly lifting a level with price
failing to advance, because a large seller is absorbing. This is Carmine's
trapped-participants/absorption verbatim in substance — an independent
arrival on the same mechanism.

**A liquidity block consumed in real time** is shown at 11:32.

**`PbD` is never mentioned or expanded here** (Gemini's uncertainties field,
unprompted). Branding `WORLD CLASS EDGE` at 17:23.

**No entry/stop/target rules, no R:R, no win rate, no trade.**

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** One standardised
  orderflow-focused wide pass, identical question across all 19 sweep videos
  for comparability. Verdict: absorption independently derived (matches Carmine); front-running-as-magnet is new to the corpus. Still no rules.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Front-running (trade *toward* a large resting order) is this channel's
  addition to the corpus — Carmine only fades absorption, never trades to it.
- Gemini confirmed unprompted that PbD is not expanded here; the definition
  must be sought in the PbD cluster.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-072106 [full] gemini-3.6-flash (tok 97491/1005) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072106/
