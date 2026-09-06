# Video: vl01TiVTuoQ

- **URL:** https://www.youtube.com/watch?v=vl01TiVTuoQ
- **Title:** Master Orderflow Trading: The Ultimate Step-by-Step Guide 2026
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026 · **Duration:** 12:03
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**The corpus's cleanest definition of order flow.** Spoken at 00:42, verbatim:

> *"Orderflow doesn't just show you where prices were, but who is currently
> buying, who is currently selling, and how aggressively."*

That is Carmine's Time & Sales premise (ep. 2 — "who is the aggressor")
stated in one sentence, and it is the best single-line definition in the
corpus. Opening framing at 00:05: candlesticks are guessing, footprint is
knowing. On-screen agenda (00:12): `1. Orderflow 2. Professionals 3. Entry`.
The retail hook at 00:36: `always the same question: "Why does the market
always move against me?"`

**Bid and ask defined plainly** (02:05, 02:17) — the bid is where something is
offered for purchase, the ask where orders are offered for sale.

**Real order-book sizes, by instrument** — the most useful content here,
because it calibrates what "large" means per market:

| Instrument | Observed book sizes | t |
|---|---|---|
| S&P 500 (ES) | a single ask-side order of **325 contracts** | 03:56 |
| DAX (FDAX) | `1, 1, 2, 4, 3, 5, 33` | 04:02 |
| Bond futures | **5,000–6,000** per side | 09:23 |
| Gold | `2 or 4 or 6` | 09:39 |

A price reference of **7596.25** is called out at 08:07 where a large order
executed.

**Spoofing, handled honestly** (06:49): *"Spoofing used to exist and probably
still does sometimes… but exponentially large orders are usually real."* He
neither dismisses the objection nor lets it void the method.

**Level 2 vs Level 3** (07:30) — Level 3 showing up to 100 orders deep. The
corpus has not previously distinguished these.

**Platform is German-language**: the order panel at 06:08 reads `Konto,
Schließen, Break-Even (b), Kauf, Verkauf, Kauf MKT, Verkauf MKT, Kauf ASK,
Verkauf ASK, Kauf BID, Verkauf BID, Cancel All, Reverse, Nur Verträge, SL/TP,
Bearbeiten` — a DOM-execution front end (StereoTrader-class), not a stock
TradingView layout.

**No trade, no numbers on risk.** No entry/stop/target rules, no R:R, no win
rate. This is a tour of the instruments, not a strategy.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** One standardised
  orderflow-focused wide pass, identical question across all 19 sweep videos
  for comparability. Verdict: the corpus's best one-line definition of order flow, plus per-instrument book-size calibration. No tradeable rules.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- German execution panel visible (`Kauf`/`Verkauf` = buy/sell) — a DOM front
  end, not TradingView. Ask for German verbatim before translation.
- Use the per-instrument size table here as the corpus's reference for what
  counts as a large resting order outside ES.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-072014 [full] gemini-3.6-flash (tok 66550/1593) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072014/
