# Video: 00QtD-RosLg

- **URL:** https://www.youtube.com/watch?v=00QtD-RosLg
- **Title:** Everything you've learned about trading is wrong...
- **Channel:** Carmine Rosato — "Trading Orderflow Series" ep. 8 (final; title card "COMMON MISTAKES TRADERS MAKE AND HOW TO FIX THEM")
- **Uploaded:** 2024-11-25 · **Duration:** 26:24 (1584 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #9 · bead dr-08s.8
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it is.** A recap of episodes 1–7, not new material. Despite the
title card, no enumerated list of "mistakes" is presented (verified by
zoom 00:00–01:50); the mistakes are the retail behaviours already covered
(buying breakouts, longing trendlines, shorting breakdowns, using indicators
instead of order flow). Structure, with the episode each segment reprises:
01:41 auction slide + real-estate/AAPL ladders (ep. 1, 5) · 06:02 funnel
(ep. 1) · 06:55 "Who is in control of price?" · 09:13 candlestick-vs-
footprint diagram · 10:20 Trapped Traders / Absorption (ep. 2, 3) · 11:56
Oct 3 2024 trade log + −735/−1171 footprint (ep. 2, 7) · 13:46 heatmap
near 5812 (ep. 3's Oct 9 trade) · 14:44 Retail vs Institutions (ep. 4) ·
17:02 How Does Retail Trade? (ep. 4, 5) · 17:52 What Makes A Good S/R
(ep. 5) · 19:29 Obvious vs Non-Obvious (ep. 5) · 20:06 High Volume
Reversal Setups (ep. 6) · 22:40 3 Pillars / CLC (ep. 7) · 23:21–25:04 "The
Now" execution screen + Time & Sales at 5044–5048 (ep. 7).

**New content (verified by frames, Claude direct):**
- 06:55 *Who is in control of price?* — over the ES 1-min chart reused
  since ep. 1 (labels `Price Level12 ($5818.25)`, `0p ($5806)`,
  `15m ($5771)`, `RESISTANCE ($5730)`; axis 5720–5820). Rule (07:14–07:48):
  most losing trades are shorts taken while buyers control price or longs
  while sellers do; a candlestick chart cannot show control — order flow
  can; short at the supply box only if sellers are strong there, otherwise
  pass. `frames-653-703/f_0003.jpg`.
- 09:13 *CANDLESTICK VS FOOTPRINT CHART* — one green candle beside a
  21-row bid×ask ladder: HIGH → 0×177; 529×1043; 1284×1148; CLOSE →
  688×1514; 2392×1956; 2477×2402; 1329×2126; 2038×2178; 1227×1736;
  2594×1432; 458×473; 2124×1808; 749×864; 0×512; 0×71; 104×123; 405×534;
  OPEN → 1157×1409; 231×229; 417×473; LOW → 1×0. Left = market orders that
  hit the bid (sellers), right = market orders that lifted the offer
  (buyers). `frames-910-922/f_0004.jpg`. *Gemini misread 5 of 21 rows
  (e.g. CLOSE row as 1466×2315, OPEN row as 417×473, dropped 1157×1409).*

**Everything else** is the same slides and examples verified in the
earlier cards; see `videos/{QaNPAaEnB5E,eJZhX6Xz4cU,tgQC7Dpcc8A,0QlGCz6U_1g,
5qBo04SMUFc,w7tvJCuZAq8,7facFfjQ0UE}/CARD.md`. Wide-pass reads of the
reused items (Net P&L $21,750.00, Trade Risk $2,250.00, "-735 and -1171
delta AS market is at the LOW") match those cards.

**Gemini errors caught:** three of four zone labels garbled by reading
`$5` as `60` ("Tp (6080)" for `0p ($5806)`, "15m (60775)", "RESISTANCE
(60720)"); footprint diagram 5/21 rows wrong and row count given as 20.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: identify what is new vs recap; verify the new
  slides. Wide + 3 zooms (00:00–01:50, 06:40–08:00, 09:00–10:40) + 20
  frames, checked directly (no subagent — recap content is verified by
  cross-reference to earlier cards). Verdict: two new slides, both
  verified; label-glyph pattern discovered. Card closed. Runs:
  `runs/20260828-124558` (wide), `-1248*`/`-1249*` (zooms).

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Recap episode: every chart/slide is a rerun; verify by cross-reference,
  not by re-pulling frames.
- The ES 1-min chart with `15m ($5771)` / `RESISTANCE ($5730)` is the
  channel's stock backdrop (eps. 1, 4, 8).

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-124558 [full] gemini-flash-latest (tok 144477/1552) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-124558/
- 20260828-125008 [00:00-01:50] gemini-flash-latest (tok 10270/674) — Q: Paraphrase the introduction: what does the presenter say this episode covers, an… — runs/20260828-125008/
- 20260828-125032 [06:40-08:00] gemini-flash-latest (tok 7554/893) — Q: Transcribe verbatim the 'Who is in control of price?' slide and every label, pri… — runs/20260828-125032/
- 20260828-125112 [09:00-10:40] gemini-flash-latest (tok 9391/1598) — Q: Transcribe verbatim every label and number on the 'CANDLESTICK VS FOOTPRINT CHAR… — runs/20260828-125112/
