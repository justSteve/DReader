# Video: vl01TiVTuoQ

- **URL:** https://www.youtube.com/watch?v=vl01TiVTuoQ
- **Title:** Master Orderflow Trading: The Ultimate Step-by-Step Guide 2026
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-07-01 · **Duration:** 12:03 · **Views:** 11,008
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**The corpus's cleanest definition of order flow.** Spoken at 00:42, verbatim:

> *"Order flow doesn't just show you where prices were, but who's buying,
> who's selling, and how aggressively."*

*(Wording note, 2026-09-06: an earlier version of this quote carried
"currently" twice and was labelled verbatim. YouTube's captions have no
"currently"; Gemini's transcription does. Both are machine ears on AI-dubbed
audio and no frames exist, so neither is authoritative — the caption wording is
used here as the more conservative of the two. The sense is identical.)*

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
| DAX (FDAX) | single digits, **1–5 per level** — the ask column reads 1, 1, 2, 4, 3, 4, 5, 3, 3 upward from 25152; no "33" anywhere in the book (frames 2026-09-08, `frames-356-408/f_0007.jpg`) | 04:02 |
| Bond futures | **5,000–6,000** per side | 09:23 |
| Gold | `2 or 4 or 6` | 09:39 |

A price reference of **7596.25** is called out at 08:07 where a large order
executed.

**Spoofing, handled honestly** (06:48–07:01). The card previously spliced this
into a single sentence; his full wording is *"I know that spoofing used to
exist and probably still does sometimes, and that it's possible for such an
order to be a fake order and get pulled. But, let's stick with exponentially
large orders. They're usually real because someone has the ambition to do
something there."* Earlier rendering: *"Spoofing used to exist and probably
still does sometimes… but exponentially large orders are usually real."* He
neither dismisses the objection nor lets it void the method.

**Level 2 vs Level 3** (07:29–07:43) — he describes a book showing *"many more
orders there… up to 100"*, immediately hedged: *"**I don't even know exactly how
many** you can have displayed."* **Terminology caution added 2026-09-06:** what
he describes is a *deeper Level 2 display* — the same thing
[Vd83oo_geMk](../Vd83oo_geMk/CARD.md) calls 20 rows settable to 100 — whereas
vendor "Level 3" means order-by-order data. This card previously presented his
usage as the standard distinction. The
corpus has not previously distinguished these.

**Platform is German-language**: the order panel at 06:08 reads `Konto,
Schließen, Break-Even (b), Kauf, Verkauf, Kauf MKT, Verkauf MKT, Kauf ASK,
Verkauf ASK, Kauf BID, Verkauf BID, Cancel All, Reverse, Nur Verträge, SL/TP,
Bearbeiten` — a DOM-execution front end. *(Corrected 2026-09-06: previously guessed as "StereoTrader-class". The run's own note says the layout resembles ATAS/Sierra Chart, and the identical German panel — `Schließen`, `Kauf MKT` — is identified as the **ATAS DOM Trader** on [yWO8hVpRXeY](../yWO8hVpRXeY/CARD.md). ATAS is the better inference.)* Not a stock
TradingView layout.

**No trade, no numbers on risk.** No entry/stop/target rules, no R:R, no win
rate. This is a tour of the instruments, not a strategy.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** One standardised
  orderflow-focused wide pass, identical question across all 19 sweep videos
  for comparability. Verdict: the corpus's best one-line definition of order flow, plus per-instrument book-size calibration. No tradeable rules.
- **2026-09-08 — frame pull 03:56–04:08 (dr-gm5).** Settled the DAX-ladder digit
  the 2026-09-06 audit left open: the FDAXM6 ask column is single digits
  throughout (max 5); the captions' "3 3" are two levels, the carded "33" was
  Gemini joining them. Findings row corrected.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- German execution panel visible (`Kauf`/`Verkauf` = buy/sell) — a DOM front
  end, not TradingView. Ask for German verbatim before translation.
- Use the per-instrument size table here as the corpus's reference for what
  counts as a large resting order outside ES.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-072014 [full] gemini-3.6-flash (tok 66550/1593) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-072014/
