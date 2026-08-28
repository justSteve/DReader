# Video: w7tvJCuZAq8

- **URL:** https://www.youtube.com/watch?v=w7tvJCuZAq8
- **Title:** You've Been Using Volume WRONG This Whole Time...
- **Channel:** Carmine Rosato — "Trading Orderflow Series" ep. 6
- **Uploaded:** 2024-11-13 · **Duration:** 31:28 (1888 s)
- **Playlist:** PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ #7 · bead dr-08s.6
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** Volume-by-price (footprint, heatmap, DOM) over
volume-by-time; two frameworks: (A) high-volume REVERSAL at breakouts —
aggressive volume into a level with no continuation = trapped traders,
fade it; (B) CONTINUATION — after a strong move, buy the pullback / short
the pop when the volume spike on the pullback is absorbed. Custom volume
study on every chart: `BuyingVsSelling_Carmine (yes, yes, yes, 200, yes,
yes)` (ThinkorSwim-style, no ticker/timeframe chrome; ES by price level).

**A. High Volume Reversal Setups (01:16 slide, verified word-for-word).**
"How many times have you tried to BUY a breakout on high volume? … BOUGHT
the BREAKOUT for the market to reverse and stop you out? If you BUY every
breakout you are positioning yourself to become TRAPPED by smart money
(patient traders) and GIVING THEM your LIQUIDITY. I AM ALWAYS LOOKING FOR
REVERSALS FIRST on breakouts….." Spoken 02:43: reversal-first ~99% of the
time on the first test of a breakout.
- Example 1 (03:19 → 06:39): "Strong opening rally candle" into "Previous
  day resistance / HIGH" with "VOLUME SPIKE"; volume box `Daily Avg:
  1,328,6x3 | Today: 754,441`; chart axis **5850–5935**, tooltip Hi
  5927.25. Footprint (10:00–10:40, 5-min bars, axis 5648.50–5664.00, cells
  delta|volume): **+1319 | 1775 at 5660.00** (10:10; presenter says "1700
  / +1300"), **+620 | 620 at 5661.50** (top of the 10:25 bar — 100 % at
  the ask), **+577 | 1245 at 5660.00** (10:25; "1200"), **+585 | 1015 at
  5655.00** (10:20). Rule (07:05): heavy aggressive buying + positive
  delta at the breakout with no upward continuation = passive sellers
  absorbing, buyers exhausted → fade/short into the trapped buyers.
  **Verified: frames** (`frames-615-640/f_0004.jpg`, `f_0013.jpg`).
- Example 2 (10:14–10:56): Bookmap-style heatmap (no chrome), axis
  5649.75–5670.00 in 0.75 steps, white line ≈5664.9: green buy bubbles
  cluster at/above the line, price then grinds to ~5650 with red bubbles.
  Rule: aggressive buying hitting the ask with no follow-through = should
  go down, not up. **Verified: frames** (`frames-1010-1025/f_0007.jpg`).
- Example 3 (14:06–15:33), "Would You Take This trade short?": obvious
  SUPPORT break (axis 5575–5592, volume tag 77,676) on the biggest volume
  bar — "directly after volume hit its highest on breaking support was
  literally the low". Rule: the last seller sells into absorption; no
  selling power left → reversal long, not short. Bookmap follow-up
  (5619.75–5639.25, support 5628.75) **unverified**.
- 15:35 "Why Does Price Change Directions?" — ep. 4's bait-fish slide,
  reused with the diagram (verified).

**B. Continuation Volume Setups (16:43 slide, verified).** "How many
times have you tried to BUYING A DIP / catching a falling knife because
you spot LARGE VOLUME but end up losing? Usually rallies/pops after a
strong drop are GREAT to SHORT into; usually sell-offs/quick pullbacks are
GREAT to BUY into for more continuation."
- Example (18:46, verified word-for-word): "Strong rally. Gauging to see
  if market continues or FAILS" → "Trendline break – many are
  shorting/selling. Confirmed by volume spike. Good opportunity to BUY";
  axis 5724–5752, 9:25–10:00. Rule: retail shorts the trendline break;
  the spike is their selling being absorbed by passive buyers → long for
  continuation. Footprint lowest print "178 / −178" (spoken; unverified).
- 23:25 slide "Break of Resistance/Support Continuation" (bullets in by
  23:29, verified): "I RARELY EVER simply buy when resistance breaks … I
  rather let it BREAK, and BUY the pullback or SHORT the rally. 1 – if
  market breaks the level it shows buyers/sellers are strong. 2 – once #1
  is true, if a rally or drop forms and buyers/sellers DEFEND price and
  resistance/support flips, those participants are EVEN MORE POWERFUL."
- Example (27:12–28:04): RESISTANCE zone ≈5842.5–5846 flips to support;
  footprint column 12:45:58 (axis 5842–5859): **−750 | 1568 at 5848.50**
  and **−538 | 1498 at 5847.25** — heavy selling into the flipped level
  with no breakdown = absorption → long on the retest. Text box 28:04:
  "Instead of getting long as SOON as it breaks, I will look for signs of
  buyers BEFORE it breaks, to get long and be in BEFORE the move."
  **Verified: frames + parity** (`frames-2710-2730/f_0007.jpg`; Gemini's
  "−583" fails delta≡volume mod 2 against 1498 — pixels say −538).
- Risk/reward drawing (30:00–30:18): early entry at the ~10:00 pullback
  (~5836–5838) vs breakout entry (~5847); two green boxes to the same
  ~5861 ceiling — the later entry's reward box is visibly shorter and its
  stop (hooked line to ~5825) farther. **No numbers, ratios or R figures
  written** (verified). Spoken: the early entry's stop sits under the
  pullback low; the breakout entry must risk down to the base.

**Concrete parameters:** none numeric beyond the examples; "200" in the
custom study's parameters; 5-min footprint bars in example 1.

**Next episode (30:57):** ep. 7 — confirmation, execution, stops/targets,
management.

**Gemini errors caught:** −583 (actual −538); rounded figures reported as
values (1700/1300 vs 1775/1319; 1200 vs 1245); 03:19 price axis given as
5645–5690 (actual 5850–5935 — bled from the later footprint); slide
timestamps 2–4 s early (text not yet on screen); seven axis labels
silently dropped on the Bookmap list; "5830–5895" axis (actual 5842–5859).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28** — Aim: extract both volume frameworks and verify every
  footprint figure. Wide + 6 zooms + 76 frames + Opus verifier (37 tool
  uses, 70 min). Verdict: slides and chart annotations exact; footprint
  cells right where the presenter circles them, wrong by transposition
  once (caught by parity); one axis bled across charts. Card closed.
  Runs: `runs/20260828-120624` (wide), six zoom dirs `-1209*`…`-1212*`.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Custom study `BuyingVsSelling_Carmine (…)` labels every volume panel —
  a reliable fingerprint for this channel's ThinkorSwim charts.
- Footprint cells are `delta | volume`; the presenter circles the cells he
  cites — a frame at the circle moment pins the cell unambiguously.
- He rounds aloud (1775→"1700", 1319→"1300", 1245→"1200"); on-screen
  values are the record.
- Level labels here are bare ("RESISTANCE", "SUPPORT") — no `$price`
  parentheticals, hence no glyph-confusion risk on this episode.
- Slide bullets animate in over ~4 s after the title.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-120624 [full] gemini-flash-latest (tok 172141/1517) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260828-120624/
- 20260828-121002 [03:00-07:30] gemini-flash-latest (tok 24901/1161) — Q: For the false-breakout example: transcribe every label, price level, zone name a… — runs/20260828-121002/
- 20260828-121024 [09:50-11:40] gemini-flash-latest (tok 10293/809) — Q: Describe the heatmap/Bookmap example: platform, instrument, timeframe, every vis… — runs/20260828-121024/
- 20260828-121049 [13:40-15:35] gemini-flash-latest (tok 10757/737) — Q: For the support-failure example: transcribe every label, price level, zone name,… — runs/20260828-121049/
- 20260828-121109 [18:20-20:40] gemini-flash-latest (tok 13032/1696) — Q: For the continuation pullback example: transcribe every label, price level, zone… — runs/20260828-121109/
- 20260828-121140 [26:30-28:40] gemini-flash-latest (tok 12126/702) — Q: Transcribe every volume and delta number, price level and annotation on the foot… — runs/20260828-121140/
- 20260828-121212 [29:30-31:20] gemini-flash-latest (tok 10304/1100) — Q: Transcribe every number, price level, R-multiple, ratio or annotation on the ris… — runs/20260828-121212/
