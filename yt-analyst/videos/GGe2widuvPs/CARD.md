# Video: GGe2widuvPs

- **URL:** https://www.youtube.com/watch?v=GGe2widuvPs
- **Title:** How Price Actually Moves — The Deep Mechanics Nobody Teaches (Video 6)
- **Channel:** Smart Money Decode X (logo bottom-right; no presenter on camera)
- **Uploaded:** 2026-08-14 · **Duration:** 15:21 (921 s)
- **Playlist:** PLU9kIorYkc18 #6 · bead dr-8qq.6
- **First analyzed:** 2026-08-29
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What it teaches.** The order book as the engine of price: market
orders consume resting limit orders and the last fill *is* the price;
the bid–ask spread; why price moves fast through sparse levels and
grinds through dense ones (volume profile, HVN/LVN); the mechanics of a
liquidity sweep (stops = resting market orders the institution needs);
why support/resistance holds and then fails (each visit consumes
orders); and a reframing of every chart feature as an order-book
fingerprint. Numbers are worked examples drawn on slides — several are
ladders that Gemini skipped entirely and had to be read from frames.
Whiteboard slides + AI mock charts.

**Structure and content (slide text verbatim; "verified" = frames):**

- **00:00–01:29 hook.** "SOMETHING SPECIFIC HAPPENED HERE" — not "RANDOM /
  LUCK / NO REASON" (00:01–00:04); "THE ENGINE BEHIND EVERY MOVE —
  MECHANICAL / REPEATABLE / SAME LOGIC" (00:11); "MYSTERY → READABLE";
  title (00:35); "FROM VIDEO 1 — AGGRESSION MOVES PRICE" (00:49); "VIDEO 6
  — FULL MECHANICS" (01:03); two puzzles on mock charts: "SAME VOLUME —
  DIFFERENT MOVEMENT. WHY?" (01:08) and "SHARP REVERSAL HERE — / CLEAN
  BREAK HERE. WHY?" with "Resistance at $69,500 / Support level: $67,000"
  (01:18); "THE ORDER BOOK — THE REAL ENGINE: ORDERS IN → ORDER BOOK →
  PRICE MOVEMENT OUT" (01:29–01:33).
- **01:38 "LIVE — EVERY PRICE — EVERY RESTING ORDER" — verified
  (frames-136-142 f_0004), 15-row ladder, headers BIDS | PRICE | ASKS:**
  asks 103.50 ×15 · 103.25 ×10 · 103.00 ×120 · 102.75 ×80 · 102.50 ×35 ·
  102.25 ×15; **102.00 empty (the spread)**; bids 101.75 ×15 · 101.50 ×70 ·
  101.25 ×130 · 101.00 ×170 · 100.75 ×180 · 100.50 ×180 · 100.25 ×210 ·
  100.00 ×345. Gemini's 14 sized rows were digit-perfect; it omitted the
  empty spread row and the headers.
- **02:00 "SELL ORDERS — ABOVE CURRENT PRICE" — frames only (f_0001):**
  a 9-row mock stack Gemini never mentioned (sells $1.5 ×300, $2.51 ×200,
  $7.01 ×300, $6.50 ×400, $6.00 ×1000; buys $2.00 ×1000, $7.2 ×1000, $2.00
  ×200, $1.10 ×30 — AI-generated, non-monotonic; decor).
- **02:01–02:07 — verified (frames-200-210).** "PRICE = THE MIDDLE": SELL
  ORDERS (ASK) 101.50 ×100 · 101.00 ×70 · 100.50 ×10 / CURRENT PRICE / BUY
  ORDERS (BID) 99.50 ×20 · 99.00 ×100 · 98.50 ×60 (02:01). "ORDER BOOK
  SKETCH" PRICE | QUANTITY: ask 101.50 ×100 · 101.45 ×250 · 101.40 ×500 ·
  101.35 ×100; bid 101.30 ×100 · 101.25 ×250 · 101.20 ×500 · 101.15 ×100;
  "CURRENT MARKET PRICE (approx. 101.32)"; "NEXT PRICE = THIS ORDER WHEN
  HIT" (02:07). All digits exact.
- **02:16–02:53 the mechanism — verified (frames-214-220).** "$50,000
  CURRENT — RESTING SELL AT $50,010" (02:16, verified); "MATCHED AT
  $50,010 — TRANSACTION COMPLETE" (02:28); "ONE TRANSACTION — PRICE MOVED
  $10" (02:35); **rule:** "MARKET ORDER + RESTING ORDER = PRICE MOVEMENT"
  (02:53) — "HOW EVERY PRICE MOVEMENT BEGINS" (02:55).
- **03:02–04:26 absorption and gaps — verified (frames-356-400).** "1
  ORDER → 1,000 ORDERS AT SAME LEVEL"; "ONE CONSUMED — PRICE STAYS — 999
  REMAIN" (03:08); "HITTING LEVEL — CANNOT BREAK — TOO MANY ORDERS
  ABSORBING" (03:20); "ABSORPTION — MARKET ORDERS VS LIMIT ORDER WALL"
  (03:28); "DENSE ORDER LEVEL = WALL — PRICE CANNOT PASS" (03:30);
  "MULTIPLE REJECTIONS — THEN BREAKS WHEN ORDERS CONSUMED" (03:35); "1,000
  ORDERS → 0 ORDERS — SUDDENLY GONE" (03:41). "ORDER BOOK: MASSIVE GAP
  DETECTED" (03:54, verified f_0001) — **the gap book, frames only:** BUYS
  $50,010 ×50 · $50,000 ×20 · $49,995 ×10 · $49,900 ×10 · $49,850 ×30 ·
  $49,800 ×10 · $49,750 ×30 · $49,700 ×40; SELLS $50,150 ×10 with a void
  below — "NEXT SELL ORDER — FAR ABOVE — GAP IN BETWEEN"; "NOTHING TO
  MATCH — PRICE JUMPS $90 INSTANTLY" (03:58, verified). (The drawn gap is
  $50,010→$50,150 = $140; the caption says $90 — the slide's own
  inconsistency.) "THIS IS A FAIR VALUE GAP — PRICE SKIPPED HERE" (04:07);
  "NOT RANDOM — LIQUIDITY DISAPPEARED: FAIR VALUE GAP = VOID WHERE NO
  RESTING LIMIT ORDERS" (04:18).
- **04:26–05:55 the spread — verified (frames-425-438).** "THE BID-ASK
  SPREAD — THE MOST FUNDAMENTAL PRICE MECHANIC": BID ↑ $50.00 / $49.95 /
  $49.90 · **$0.05 SPREAD** · ASK ↓ $50.05 / $50.10 / $50.15 (04:26);
  "EVERY PRICE — TWO SIDES: CURRENT PRICE 50,000 · BID 49,990 · ASK 50,010"
  (04:30); "BID = HIGHEST PRICE BUYER WILL PAY RIGHT NOW" — buyers A
  $10.00, B $10.25, C $10.50 = THE BID; sellers $10.75, $11.00 (04:36);
  "ASK = LOWEST PRICE SELLER WILL ACCEPT RIGHT NOW" (04:40); "SPREAD = THIS
  DIFFERENCE" (04:43); "MARKET BUY = FILLED AT ASK PRICE / MARKET SELL =
  FILLED AT BID PRICE" (04:46–04:50); "SPREAD = MINIMUM COST — EVERY TRADE
  — NO EXCEPTIONS" (04:54); "TIGHT SPREAD = HIGH LIQUIDITY — MANY
  PARTICIPANTS CLOSE TO PRICE" (05:01); "WIDE SPREAD = LOW LIQUIDITY — FEW
  PARTICIPANTS" (Ask 18.800 / Bid 18.600, 05:12); "ONE LARGE ORDER — THIN
  LIQUIDITY — LARGE PRICE IMPACT" (05:18); "LOW LIQUIDITY PERIOD — MORE
  AGGRESSIVE MOVES PER ORDER" (05:24); "ASIAN = SMALL MOVES / LONDON/NY =
  LARGER MOVES" (05:29); "SAME VOLUME — DIFFERENT TIME — DIFFERENT PRICE
  IMPACT" with 08:00 (LDN OPEN) / 16:00 (NY OPEN) / 00:00 (TKY OPEN)
  (05:52).
- **05:59–07:30 market vs limit — verified (frames-640-644, -723-727).**
  "MARKET ORDERS vs LIMIT ORDERS — THE TWO FORCES" ("EXECUTE NOW!" vs "SET
  PRICE & WAIT — PRICE: $50.00", 05:59); "INTERACTION = PRICE MOVEMENT"
  (06:06); "MARKET ORDER — AGGRESSIVE — EXECUTE NOW — CONSUMES LIQUIDITY"
  (06:11); "LIMIT ORDER — PASSIVE — WAIT HERE — PROVIDES LIQUIDITY"
  (06:23); "MARKET ORDERS — MOVE PRICE (instant execution, aggressive,
  high impact) / LIMIT ORDERS — RESIST PRICE MOVEMENT (patient, passive,
  create walls)" (06:30); "MARKET ORDERS OVERWHELM LIMITS — PRICE BREAKS
  THROUGH" (06:34); "STALL ZONE — LIMIT ORDERS ABSORB MARKET ORDER — PRICE
  STALLS" at $68,150.75 (06:41, verified; a 10-row mock bid panel beside
  it went unreported); **the three regimes:** "STRONG TREND = MARKET
  ORDERS OVERWHELMING LIMITS" (06:52); "CONSOLIDATION = SLOW MARKET ORDERS
  ABSORBED BY LIMITS" (07:01); "REVERSAL = MARKET ORDERS EXHAUSTED BY
  LIMIT CLUSTER" (07:10); "EVERY PRICE MOVE = THIS BATTLE — MARKET ORDERS
  — AGGRESSION / LIMIT ORDERS — PATIENCE" (07:19); "EVERY CANDLE = BATTLE
  RESULT FOR THAT PERIOD — BATTLE RESULT: BULLS WON, BY HOW MUCH:
  +$2,450.00" (07:24, verified).
- **07:30–09:12 speed through levels.** "WHY PRICE MOVES FASTER THROUGH
  SOME LEVELS"; "INSTANT MOVE — LARGE CANDLE — NO HESITATION" vs "SLOW
  GRIND — SMALL CANDLES — FREQUENT REVERSALS" (07:42–07:47); **rule:**
  "DENSE ORDERS = SLOW. SPARSE ORDERS = FAST." (07:53); "FEW ORDERS HERE —
  PRICE RACES THROUGH / NOTHING TO ABSORB — MARKET ORDERS FLY THROUGH"
  (07:56–08:01); "MANY ORDERS HERE — PRICE GRINDS SLOWLY" (08:10); "VOLUME
  PROFILE = MEASURES ORDER DENSITY AT EACH LEVEL" (08:25); "HIGH VOLUME
  NODE = ENORMOUS TRANSACTIONS HERE" (08:35); "PRICE RETURNS TO HVN — SAME
  RESISTANCE AGAIN" (08:45); "LOW VOLUME NODE = ALMOST NO TRANSACTIONS
  HERE" (08:58); "PRICE ENTERS LVN — MOVES FAST — NOTHING TO ABSORB"
  (09:07).
- **09:12–11:00 the liquidity sweep — verified (frames-911-915,
  -1035-1038).** Title slide "THE MECHANICS OF A LIQUIDITY SWEEP" (09:12)
  is illustrated with a **bank cash-sweep diagram** (subsidiary accounts
  $5k/$2k/$8k → "AUTOMATED TRANSFER (THE 'SWEEP')" → main concentration
  account $15k) — an AI-illustration mismatch in the source, verified
  f_0003. Then: "SWING LOW — THOUSANDS OF STOPS BELOW" (09:22); "STOP
  LOSSES = SELL ORDERS WAITING TO TRIGGER" (09:29); "INSTITUTIONAL NEED:
  LARGE SELL ORDERS TO MATCH" (09:39); "STOP CLUSTER = EXACTLY WHAT
  INSTITUTION NEEDS" (09:47); "ENGINEERED PUSH BELOW SWING LOW" (09:53);
  "ALL STOPS TRIGGERED SIMULTANEOUSLY — MASSIVE SELL WAVE" (09:57–10:02);
  "INSTITUTION ABSORBS EVERY SELL — MATCHING WITH BUYS" (10:06); "SHARP
  RECOVERY — ALL SELLING CONSUMED — INSTITUTION POSITIONED" (10:13); "SAME
  MOMENT — OPPOSITE OUTCOMES: RETAIL STOPS — OUT / INSTITUTION — FULLY IN"
  (10:19); "SELLING EXHAUSTED — INSTITUTION IN — MARKUP BEGINS" (10:24);
  "NOT ILLEGAL MANIPULATION" (10:31); "MECHANICAL NEED — NOT MANIPULATION
  … MECHANICAL REQUIREMENT: EQUAL OPPOSING FLOW" (10:36, verified; the
  drawing carries AI-garbled labels "CHEOSING MATERIAL FLOW UITS", "PIPES
  WITD MATERIALS"); "SIZE PROBLEM (VIDEO 3) … SWEEP = SOLUTION" (10:52);
  "THIS WICK = SPECIFIC TRANSACTION — NOT RANDOM — Large OTC Transaction:
  1,200 BTC @ $62,500" (11:00, verified f_0003).
- **11:16–12:53 S/R mechanics — verified (frames-1155-1158).** "WHY S&R
  WORKS — AND WHY IT STOPS WORKING" (support: demand > supply → reverses
  up; resistance: supply > demand → reverses down; failed support =
  breakdown, failed resistance = breakout; 11:16); "SUPPORT = LARGE
  RESTING BUY ORDER CLUSTER HERE" (11:20); "SELLS ABSORBED BY BUY CLUSTER
  — PRICE REVERSES" (11:39); "BUY ORDERS CONSUMED — SUPPORT FAILS" (11:51);
  "EACH VISIT CONSUMES ORDERS: VISIT 1 Full Buy Order Block → VISIT 2
  Smaller Block → VISIT 3 Even Smaller/Depleted" (11:56, verified);
  "ORDERS DEPLETED — PRICE FALLS STRAIGHT THROUGH" (12:04); **rule:** "MANY
  TESTS = DEPLETED ORDERS = EVENTUAL BREAK" (12:25); "NOT TA FAILURE —
  MECHANICAL CONSUMPTION" (12:30); "EVERY MOVE = MARKET ORDERS CONSUMING
  RESTING ORDERS" (12:47); "LARGE FAST CANDLE = THIN RESTING ORDERS AT
  THESE LEVELS" (12:53).
- **13:03–15:21 fingerprints and close — verified (frames-1430-1434,
  -1454-1458).** "SMALL CHOPPY CANDLES = DENSE RESTING ORDERS HERE"
  (13:03); "SHARP MOVE + IMMEDIATE REVERSAL = RESTING ORDERS ABSORBED ALL
  INCOMING" (13:11); "HELD MANY TIMES — THEN BROKE — ORDERS FINALLY
  CONSUMED" (13:22); pattern glossary (13:35): CONSOLIDATION /
  BREAKOUT / LIQUIDITY SWEEP / TREND REVERSAL as order-book events;
  "VIDEO 4 SHAPES = VISUAL EXPRESSION OF MECHANICS: Marubozu =
  overwhelming market orders · Doji = equal market and limit orders ·
  Long wick = absorbed then rejected" (13:40); "VIDEO 5 TIMEFRAMES = WHICH
  LEVEL OF MECHANICS" (13:44); "EVERY FUTURE CONCEPT = ORDER BOOK TOOL:
  Market Structure · Liquidity Zones · Order Blocks · Volume Analysis"
  (13:54); "FINGERPRINTS OF ORDER FLOW — NOT THE ORDER FLOW ITSELF"
  (14:05); "GUESSING vs UNDERSTANDING — THIS SKILL IS THE DIFFERENCE"
  (14:11); "NOT A LINE — A CONTINUOUS BATTLE SCOREBOARD" (14:20); "EVERY
  CANDLE = BATTLE REPORT — WINNER: BULLS (+3.2%) · MARGIN: $2,150 Vol. ·
  RESISTANCE ENCOUNTERED: Heavy Selling @ $71,200" (14:31, verified);
  "EVERY WICK = FAILED ATTACK / EVERY BREAKOUT = DEFENSE OVERWHELMED /
  EVERY REVERSAL = SUCCESSFUL DEFENSE" (14:34–14:39); "RECORD OF ALL
  PARTICIPANT DECISIONS — DIFFERENT SIZES, INTENTIONS, INFO" (14:48); "WHO
  HAS THE ADVANTAGE RIGHT NOW? READ THE RECORD: Series of Lower Highs ·
  Lower Lows · Break of Key Support Level ($69,000) · ADVANTAGE: BEARS"
  (14:55, verified); "POSITION BEFORE THE CROWD SEES IT" (15:00); comment
  prompt "WHICH CHANGED YOU MOST? ORDER BOOK MECHANICS / BID-ASK SPREAD /
  LIQUIDITY SWEEP EXPLANATION" (15:05); "STAY DISCIPLINED — VIDEO 7"
  (15:17).

**Numbers.** Ladders: every transcribed row exact (28/28); three whole
ladders omitted (02:00, 03:56, 06:41) and recovered from frames. Slide
arithmetic: $50,000→$50,010 = $10 ✓; $50.00/$50.05 = $0.05 ✓; 5k+2k+8k =
15k ✓; the gap book's $50,010→$50,150 = $140 vs the "$90" caption ✗
(source error). No performance claims.

**Not specified:** any way to *see* the order book on a chart beyond
"volume profile" and candle shape; no depth, no thresholds.

**Verification.** 63 frames at 1 fps over 13 windows (01:36–01:42,
02:00–02:10, 02:14–02:20, 03:56–04:00, 04:25–04:38, 06:40–06:44,
07:23–07:27, 09:11–09:15, 10:35–10:38, 11:13–11:18, 11:55–11:58,
14:30–14:34, 14:54–14:58). Opus verifier viewed 19 frames: AGREE on 12
of 13 items (one word: "CROSSING" → CHEOSING); three ladder omissions
found. Runs: 070908 (wide, 84.2K tokens) + nine zooms 072212…072246.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-29** — first contact, playlist pass (dr-8qq). Wide pass, nine
  zooms, 13 frame windows, Opus second reader. Verdict: mechanism and
  rules captured; three numeric ladders recovered from frames; card
  closed. Cost ≈ 170K prompt tokens.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- Hand-lettered ladders on this channel are large and high-contrast:
  Gemini's per-row accuracy was 100 % (28 rows) — better than the
  20–25 % error seen on platform footprints. The failure mode moved to
  **omission**: it skipped three grids outright. When the narration
  implies a book is on screen, pull frames regardless of what the zoom
  returned.
- Two source-side errors worth knowing before quoting the video: the
  "$90 jump" caption sits on a drawn $140 gap, and the "liquidity sweep"
  title is illustrated with a corporate cash-sweep diagram.
- Series cross-refs: "FROM VIDEO 1 — AGGRESSION MOVES PRICE"; "SIZE
  PROBLEM (VIDEO 3)"; video 4's candle shapes and video 5's timeframes
  are re-derived here as order-book consequences.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260829-070908 [full] gemini-flash-latest (tok 84153/1959) — Q: In your own words, what does this video teach? Give its structure in order with … — runs/20260829-070908/
- 20260829-072212 [01:30-03:00] gemini-flash-latest (tok 8492/1123) — Q: Transcribe verbatim every label, price level and number on the order-book diagra… — runs/20260829-072212/
- 20260829-072212-2 [02:55-04:30] gemini-flash-latest (tok 8918/1151) — Q: Transcribe verbatim every slide, label, price and number in this window with tim… — runs/20260829-072212-2/
- 20260829-072218 [00:00-01:35] gemini-flash-latest (tok 8919/1225) — Q: Transcribe verbatim every slide, label and annotation in this window with timest… — runs/20260829-072218/
- 20260829-072224 [05:55-07:35] gemini-flash-latest (tok 9372/1327) — Q: Transcribe verbatim every slide, label and number in this window with timestamps… — runs/20260829-072224/
- 20260829-072225 [04:25-06:00] gemini-flash-latest (tok 8918/1503) — Q: Transcribe verbatim every slide, label and number in this window with timestamps… — runs/20260829-072225/
- 20260829-072235 [11:15-13:00] gemini-flash-latest (tok 9827/1087) — Q: Transcribe verbatim every slide, label and number in this window with timestamps… — runs/20260829-072235/
- 20260829-072235-2 [07:30-09:15] gemini-flash-latest (tok 9840/985) — Q: Transcribe verbatim every slide, label and number in this window with timestamps… — runs/20260829-072235-2/
- 20260829-072236 [09:10-11:20] gemini-flash-latest (tok 12105/1709) — Q: Transcribe verbatim every slide, label and number in this window with timestamps… — runs/20260829-072236/
- 20260829-072246 [12:55-15:21] gemini-flash-latest (tok 13554/2403) — Q: Transcribe verbatim every slide, label, list item and number in this window with… — runs/20260829-072246/
