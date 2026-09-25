# Video: 9P-u7MWosFo

- **URL:** https://www.youtube.com/watch?v=9P-u7MWosFo
- **Title:** Market Mechanics Ep 9: Fair Value Gaps / Imbalance
- **Channel:** The Trading Geek (@TheTradingGeek) — Brad Goh, "1% Club" mentorship / EdgeFlo
- **Category:** Trading
- **Uploaded:** 2026-05-24 · **Duration:** 31:03 (1863 s) · **Views:** 237,250
- **First analyzed:** 2026-09-16
- **Status:** closed
- **Bead:** dr-oj9 (grade for clarity + alignment to the orderflow corpus)
- **Series:** "Market Mechanics Mentorship", ep. 9 of a numbered course; sibling card [`TthzSVTzWoE`](../TthzSVTzWoE/CARD.md) (ep. 13)

## Findings
_(curated by Claude Code: verified findings with timestamps)*

**Identity and commerce.** Presenter is **Brad Goh** (description: Instagram
`brad.goh`, X `bradgohtrades`, live-trading channel `@bradgtrades`); channel
"The Trading Geek". yt-dlp reports 179 subscribers against 237K views, so
the follower count is hidden or stale — treat as unknown. Funnel in the
description: **1% Club** mentorship (`1percentclub.co`, also the watermark on
every chart), **EdgeFlo** ("my trading superapp"), and an **Eightcap**
broker affiliate link (a CFD/forex broker). The video itself carries no
pitch beyond *"in the next lesson"* and the closing tag *"you're just one
trade away"* (30:55). No track record, P&L or win rate is claimed anywhere.
**Verified: description + transcript.** Gemini's wide pass attributed the
series to "Rayner Teo (or associated educator)" in the sibling video — a
confabulation; nothing on screen or in audio says so.

**Instrument and platform (frame-verified, `frames-720-740/f_0003.jpg`).**
TradingView in Chrome, `EURUSD · 15 · FOREXCOM`, chart dated `Tue 21 Apr
'26`, layout `Unnamed`, watermark `1PERCENTCLUB.CO`. The wide pass said
"FXCM"; the legend reads FOREXCOM. Every example in the video is spot forex
on a 15-minute chart; the 15:39 "live trade breakdown" runs in TradingView
**bar replay** — frame-verified at 16:08 (`frames-1600-1620/f_0003.jpg`:
`Replay Trading` toolbar, `Select bar · 10x · 15m`, replay cursor on
`Thu 16 Apr '26 14:30`), i.e. a curated historical walk-through, not a live
trade. The wide pass's "live" and the chapter title "Live Trade Breakdown"
both overstate it. Chart dates (16–21 Apr '26) put the recording about a
month before the 24 May upload.

**What the video is.** A definitional lesson in the ICT / Smart Money
Concepts vocabulary: *imbalance = inefficiency = fair value gap* (00:24),
*displacement*, *mitigation*, *premium and discount*, *order block* (deferred
to the next episode), *smart money*. There is no order-book quantity of any
kind: no volume, delta, footprint, DOM or tape in 31 minutes. Slide at 00:00
(wide-pass verbatim): *"an inefficient area in price where one side was so
aggressive that the market moved too quickly and did not trade efficiently
through that zone."*

**The content, as stated.**

1. *Definition* (01:57–03:05). Three-candle sequence: candle one, an
   expansion candle, candle three; the gap between the wick of candle one
   and the wick of candle three is the FVG. Bullish FVG = *"a strong move to
   the upside which leave inefficiency below"*; bearish the inverse (03:05).
2. *Identification rule* (04:56–06:43). Find the *"big juicy candlestick"*
   (*"strong displacement"*, which he glosses at 16:56 as *"really just a
   fancy word of a big bullish or bearish candlestick"*), then check whether
   the high of the preceding candle and the low of the following candle
   overlap. **No gap, no FVG** — demonstrated twice as a negative example
   (05:42–06:20, 09:55–10:31). Size is judged *"just using your naked eyes …
   compare it with the size of the candlesticks that is near it"* (17:18).
3. *Why price returns* (04:11–04:56). *"The market move from phases of
   imbalance to balance to imbalance to balance because it's actively
   seeking fair value."* Mechanism offered at 26:06: *"smart money have
   entered for a large amount of buy orders, causing price to move up so
   aggressively that it just created this gap"*, and the retrace lets them
   *"fill up the remaining orders"* (26:49).
4. *Context rules* (06:43–07:04, 11:07–12:26). Trade a bullish FVG only in
   discount and with higher-timeframe, swing and internal structure bullish;
   a bearish FVG only in premium. Worked contrast at 11:27–12:09: two bearish
   FVGs, the one *"more high up within the premium range"* with *"a more
   bigger amount of imbalance"* held, the other was *"disrespected"*.
5. *How price reacts inside a gap* (12:31–13:52). Four possibilities drawn:
   tap the edge; reach the 50% (*"the midpoint"*); reach the far extreme;
   pierce through it and *"sweep some liquidity"*. *"Do not expect the market
   to react the same way every time … never, ever assume"* (13:08–13:52).
6. *Uses* (14:25–15:36). As an entry reference (*"the minute price mitigate
   this bearish fair value gap, you can look for shorts"*) or as a target
   (*"the next opposing fair value gap"*, 20:05). Stop *"above the fair
   value gap"*, target *"like 3R or 2.5R"* (19:14) — the only numbers in the
   video, and offered as illustration, not as a rule. Entries and exits are
   explicitly deferred (19:32).
7. *Why FVGs fail* (22:26–25:20). *"It just says that it's a magnet that's
   drawing the price towards that area. Whether that area holds or not,
   that's another story"* (22:42). Worked failure at 23:41–25:20: a clean
   bullish FVG, price *"came down and break right through it"*.
8. *Core logic recap* (26:00–27:38) and course scaffolding (28:05–29:20):
   watch in order, the order block lesson depends on this one.

**Numbers.** Two: *"3R or 2.5R"* (19:14) as an example target. No price,
percentage, win rate, sample or date is spoken. Arithmetic checks are
inapplicable; the one on-screen date (21 Apr '26) is frame-read.

## Graded against the orderflow corpus

**Where it touches the corpus.** The balance/imbalance cycle (00:51, 04:11)
is Carmine ep. 1's auction premise in name: *balance = a range where buyers
and sellers agree; an event creates imbalance → new range.* SMDX defines the
FVG the same way and adds a mechanism this video lacks — *"void where no
resting limit orders"* (SMDX v6) — which is at least a statement about the
book. Brad's mechanism is the SMC one: smart money left orders unfilled and
returns for them (26:49). Nothing in the video could tell the two apart, and
nothing in it is measured.

**Where it diverges.** Carmine and Vorwald locate imbalance in the
footprint: delta, absorption, a volume tail, a level that *"the market
confirms for me"*. Here imbalance is a candle shape. The corpus's closest
relative is the SMDX series (v6 FVG, v10 BOS + retest), and against that
sibling this video is looser: SMDX ties every signal to a candle **close**;
Brad's displacement is judged by eye and his mitigation includes wick taps.

**What is honest about it.** He says three times that an FVG is not a signal
on its own (12:09, 22:26, 25:20), shows two negative examples and one
failure, and defers entries and exits rather than faking precision. That is
better discipline than most of the genre.

## Grade

**Clarity: B.** The identification rule is exact, taught with negative
examples, and a viewer could mark the same gaps he marks. It loses for
"displacement" being *"use your common sense"* (17:18), for the four
reaction modes (12:31–13:52) leaving no way to act on a gap in advance, and
for the absence of any number that could be tested. It is a definition
lesson and does not pretend otherwise.

**Alignment to the orderflow corpus: C−.** Shares the auction premise as a
slogan and nothing else. No order-book observation, no measurement, and a
mechanism (smart money returning for unfilled orders) the corpus's footprint
material neither supports nor needs. Aligned with SMDX v6 (A−), which
already covers this ground with tighter rules.

**Net.** Nothing here that the SMDX FVG card does not already hold. Keep
for the negative-example teaching pattern; do not mine.

## Sessions

- **2026-09-16** — aim: clarity + alignment grade for Steve (dr-oj9). Wide
  pass (runs/20260916-025736, 169,976 prompt tokens), full transcript read
  (5,771 words), three frame windows. Verdict: clean SMC definition lesson,
  not order flow. Closed.

## Lessons (this video)

- Chart chrome: TradingView in Chrome with the `1PERCENTCLUB.CO` watermark;
  legend `EURUSD · 15 · FOREXCOM`; date on the time axis is legible at 1080p.
  Gemini misread the data vendor as FXCM — read the legend from a frame.
- Native-English, punctuated auto-captions (Singapore-accented); clean
  substrate, no dub artefacts.
- Series is numbered and cumulative ("Market Mechanics Mentorship"); the
  description carries chapter timestamps, which match the audio.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260916-025736 [full] gemini-flash-latest (tok 169976/1551) — Q: This is episode 9 of a 'Market Mechanics' series on fair value gaps / imbalances… — runs/20260916-025736/
