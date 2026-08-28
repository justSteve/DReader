# Video: 5qBo04SMUFc

- **URL:** https://www.youtube.com/watch?v=5qBo04SMUFc
- **Title:** How To Use Support and Resistance the RIGHT Way (title card: "WHY I BELIEVE SUPPORT AND RESISTANCE IS B*LLSHIT")
- **Channel:** Carmine Rosato — "Trading Orderflow Series" ep. 5 (handle `carminerosato`; no brand wordmark on screen — Gemini's "InvestiTrade" is unsupported)
- **Uploaded:** 2024-11-08 · **Duration:** 29:21 (1761 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #6 · bead dr-08s.5
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** Support/resistance is only meaningful when the order
flow validates it. Levels form where the last buyer buys / last seller
sells; a good level shows aggressive participants exhausting into passive
ones (volume tails, absorbed delta); a weak level is one whose bounce was
driven by aggressive buyers rather than seller exhaustion. Three ways he
trades levels, plus one trade log.

**Why levels form (03:37, 06:38; slides verified by frames).** "Why does
strong resistance form? The market moves up until the last buyer buys."
Mirror for support. Real-estate ladder $100k–$400k at 05:06 (ep. 1 reuse).
Retail slides at 01:22–03:04 reused from ep. 4.

**Good S/R = validation from order flow (08:02–13:06).** Slide verified.
Footprint (unbranded, range bars; left column = delta, right = total
volume; white line = resistance at **5665.00**, redrawn at 5664.00 on
point 3):
- Point 1 (08:38): top cell **29/29 at 5665.25** — a volume tail one tick
  above the line; aggressive buyers could not lift it. (Gemini's "5665.65"
  is not a valid price.)
- Point 2 (09:41): top **136/136**, then 333/491, 617/1409, 131/2355 —
  aggressive buying absorbed until buyers dried up. (Gemini's "followed by
  131/131" is wrong.)
- Point 3 (10:42): top **51/51 at 5663.75**, then 61/147, 167/365 — same
  exhaustion signature. (Gemini's "141/141" is wrong.)
- Point 4 (11:16): strong buying into the level — largest cell **1276/6940**
  (~5663.00) mirrored by −1276/7132 below; presenter says "over +1200"
  (spoken; no 1200 on screen); failed to break out.
- Support example (12:04–13:06): "1." and "Tail" annotations; **−451** at
  ~5737.75 (also −483, −405 nearby) absorbed at support — selling exhausted,
  passive buyers held; point 2 retest shows aggressive selling again
  failing. Axis 5730–5750.
**Verified: frames** for every number above (`frames-828-840/f_0005.jpg`,
`frames-934-944/f_0004.jpg`, `frames-1034-1044/f_0003.jpg`,
`frames-1110-1120/f_0004.jpg`, `frames-1200-1240/f_0004.jpg`).

**Weak S/R (14:25–16:32).** Slide is title-only over a chart (axis
5874–5914, SUPPORT line at 5878, lows marked 1 and 2). Rule: point 1 held
because a large seller was absorbed (big negative delta + tail); point 2
bounced on *aggressive buying* (blue positive delta at the low) — no
seller exhaustion, so the level is weak and later breaks and retests from
below. **Verified: frames** (slide/axis); footprint cells too small.

**Obvious vs Non-Obvious (16:47–17:59).** Spot non-obvious things before
they become obvious; fade what everyone else is doing ("if 90% of retail
fail, why do what 90% do?"); "I FIRST use S/R as areas where buyers/sellers
become trapped, to play reversal (profit off short-term PAIN)". **Verified:
frames.**

**How I Play Support & Resistance (20:55–25:56), verified by frames:**
1. Break of resistance which then acts as support (and vice versa) — let
   it break, enter on the retest, never the initial breakout (21:18).
2. Reversals: trapped participants — "Where there is PAIN, there is GAIN."
3. Get LONG/SHORT (with valid confirmation) PRIOR to the level breaking,
   using the level as target.
Heatmap example at 20:39 (Bookmap-style, axis 5737.50–5755.50, 09:48–10:04)
— **unverified** (no frames).

**Trade example (24:30–25:36), ES short.** Double top: **279/678 at
5668.50** (left peak) and **338/530 at 5668.50** (right peak), ~3.5 pts
above the 5665 line — aggressive buyers trapped above resistance
("Effort" annotation, unverified). Journal (TradingView pane, `ES · 5`):
Net/Gross P&L **$21,875.00**, **25** contracts, **17.5** pts, Profit Target
**5631.0**, Stop **5646.0**, Initial Target **$15,000.00**, Trade Risk
**−$3,750.00**, Planned **4.00R**, Realized **5.83R**, rating 5★. No date
shown. **Verified: frames + arithmetic** — 17.5×25×50 = 21,875; 15,000/4 =
3,750 risk = 3 pts ⇒ entry **5643.0** (derived); 5643−5631 = 12 pts =
$15,000 ✓; 21,875/3,750 = 5.83 ✓; exit ≈ 5625.5. Linkage to the double
top is inferred (chart collapses 5665→~5624 after it), not stated.

**Concrete parameters:** 3-pt stop on the example; delta/volume columns;
range-bar footprint (timestamps 7:51:31 … 10:01:37, date fragment `8-26`).

**Gemini errors caught:** 5665.65 price; two adjacent-row misreads; +279/
+338 placed at 5664–5666 (actual 5668.50); `$` prefix read as "1" in the
journal's input boxes; "Total P&L" for `Net P&L`; Trade Risk omitted by
both passes; "InvestiTrade" branding invented; resistance label position
("near 5670 on the right axis" — it's at the left end of the 5665 line).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: extract the S/R method and verify every footprint
  number and the trade log. Wide + 5 zooms + 73 frames + Opus verifier
  (37 tool uses, 70 min). Verdict: slides exact; trade log verified to the
  cent; footprint top cells right, neighbours wrong. Open: 20:25–22:45
  heatmap and "Effort" annotation unframed. Runs: `runs/20260828-114808`
  (wide), five zoom dirs `-1150*`…`-1153*`.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Footprint layout here: LEFT column = delta, RIGHT = total volume (the
  reverse of ep. 2's slide order). White horizontal line = the level.
- Journal input boxes prefix values with `$` — Gemini reads it as "1".
- The deck is unbranded; the only identity on screen is the Instagram
  follow card `carminerosato` at 1:07.
- Resistance label sits at the LEFT end of its line.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-114808 [full] gemini-flash-latest (tok 160584/2092) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-114808/
- 20260828-115036 [08:00-10:50] gemini-flash-latest (tok 15767/958) — Q: Transcribe verbatim the 'What Makes A Good Support / Resistance?' slide. Then fo… — runs/20260828-115036/
- 20260828-115108 [10:50-13:10] gemini-flash-latest (tok 13040/878) — Q: For each numbered point on the footprint charts in this window (resistance point… — runs/20260828-115108/
- 20260828-115124 [14:20-16:55] gemini-flash-latest (tok 14390/891) — Q: Transcribe verbatim the 'What Makes A WEAK Support / Resistance?' slide and ever… — runs/20260828-115124/
- 20260828-115145 [20:25-22:45] gemini-flash-latest (tok 13043/946) — Q: Describe the heatmap/bubble chart at the start of this window: platform, instrum… — runs/20260828-115145/
- 20260828-115204 [24:15-26:20] gemini-flash-latest (tok 11717/1023) — Q: Transcribe every annotation, price level, volume and delta number on the double-… — runs/20260828-115204/
