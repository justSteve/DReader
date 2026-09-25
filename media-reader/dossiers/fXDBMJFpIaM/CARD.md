# Video: fXDBMJFpIaM

- **URL:** https://www.youtube.com/watch?v=fXDBMJFpIaM
- **Kind:** youtube
- **Title:** This Order Flow Indicator Is Seriously Overpowered 👀
- **Channel:** Zeiierman Trading (@zeiiermantrading) — TradingView indicator vendor, promoting its own script
- **Category:** Trading
- **Uploaded:** 2026-09-22 · **Duration:** 5:26 (326 s) · **Views:** 4,753
- **First analyzed:** 2026-09-25
- **Status:** closed
- **Bead:** dr-w5l (credibility assessment of the indicator)

## Verdict on the question asked

**Low credibility as an order-flow tool; zero evidence as a performance
claim.** The video shows a single hand-picked trade, drawn four days after
the fact on a finished chart, and states no win rate, backtest or sample. It
never shows what the script computes. It runs on **OANDA XAUUSD spot**
(frames). That is an OTC CFD feed with no exchange trades and no aggressor
side, so whatever the script calls "delta" cannot be bid/ask order flow. It
has to be a proxy built from price and tick-count volume *(inference from the
data source; the video never shows the formula)*. The "execution algorithm"
story (01:03–02:23) is narration laid over the colours. The video never
connects it to anything the indicator measures. The video is an advert for
the channel's own product.

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**What is shown (verified: frames).** One TradingView chart for the whole
video: `Gold Spot / U.S. Dollar · 15 · OANDA`, 15-minute bars from about
16 Sep to 22 Sep 2026 (the axis reads `Thu 17 Sep '26`, `Fri 18 Sep '26`, `21`, `22`).
Price runs from about 4,240 to 4,400. The lower pane is titled **`Buy/Sell
Order (Zeiierman)`** (frames-000-030/f_0001, f_0012). The pane shows no
input values in its legend, and the settings dialog is never opened. The
chart also carries a hidden `Trend Average (Zeiierman)`, and a browser tab
reads `Breakout Probability (Expo)`. The recording was made live: the taskbar
reads 22:23–22:29 on 2026-09-22, the last price ticks 4,355.64 → 4,355.75,
and the bar countdown runs down. It is not Bar Replay.

**What it computes: not revealed.** The only statement about inputs is
spoken at 00:09: *"we have set the volume, the slow delta to 500 which is the
setting I'm using"*. The meaning is spelled out at 00:20: *"green candle means
we have bullish order flow, red candle means we have bearish order flow"*.
He then calls it *"a kind of a trend indicator, but it measures the trend
within the order flow"* (00:48). The pane draws a candle-style oscillator in
green, red and orange around a slow line, with horizontal level lines. Its
scale reads `2.50 / 2.00 / 1.50` near the top (frames), which looks like a
ratio or normalised value, not raw contracts. The description hashtags
`#CVD #VolumeDelta` but gives no formula. **On OANDA spot gold there is no
bid/ask aggressor data to compute a delta from.** TradingView's volume on
that feed is tick count. So this is necessarily an OHLCV/tick-volume proxy:
an intrabar or candle-shape split of volume into "buy" and "sell". It is the
same class of thing as the "Delta Flow" bubbles in
[8O_GIxjhLkc](../8O_GIxjhLkc/CARD.md), minus even an exchange feed.
*(Unverified as to the exact formula; the data-source constraint is
verified by the frame header.)*

**The "institutions" story is not evidence.** 01:03–02:23 spoken, a
hypothetical: *"someone is now willing to buy 200 million dollar into gold…
route this order through liquidity providers, market makers, and dark
pools… execution algorithm… they split the orders"*. The claim is that this
is *"what we are trying to measure with this indicator, whether a big order
is actually executed through execution algorithms"* (02:13). Nothing on
screen links a pane value to any executed order. A CFD dealer's quote feed
cannot see another firm's execution algorithm. This is a story, not a
measurement.

**The one trade (verified: frames + arithmetic).** It is set up at 03:00–04:04
(a run of green bars, then a *"minor short-term pressure"* red patch, a wick
that *"sweeps"* a higher low and closes back above it). Entry rule, 04:16:
*"we can take the trade on the close of the candle, we put the stop loss
below the low"*. Target: *"a new high"* (04:27). The TradingView long-position
tool is drawn at about 04:20–04:40 (frames-410-440/f_0010):

| | Price (axis) | Distance | % |
|---|---|---|---|
| Target | 4,369.656 | 28.414 | 0.655% |
| Entry | 4,341.242 | — | — |
| Stop | 4,333.497 | 7.745 | 0.178% |

It closes: 28.414 / 7.745 = **3.669**, shown `Risk/reward ratio: 3.67`.
4,369.656 − 4,341.242 = 28.414 and 4,341.242 − 4,333.497 = 7.745, both exact.
28.414 / 4,341.242 = 0.6545% and 7.745 / 4,341.242 = 0.1784%, both match.
The tool itself reads **`Closed PnL: 28.414`**: the trade had already hit
its target when he drew it. The setup is Fri 18 Sep about 08:30. The recording
is Tue 22 Sep 22:28. **This is a hindsight example, picked from four days
of finished chart.**

**Cherry-picking: visible on the same screen, never mentioned.** The chart
he scrolls through contains a counter-example. From about 09:00 to 15:00 on
22 Sep, price rallies from about 4,295 to about 4,360. Meanwhile the pane
stays mostly red/orange, with only brief green flickers (frames-000-030/f_0001,
crop of the right third). Across 21 Sep the pane is mostly red while price
chops sideways between about 4,330 and 4,380. "Trade with the colour" would
have been short into that rally. *(My read of the frames; Gemini was not
asked about it. The webcam covers the last couple of hours of the pane.)*

**Repainting: cannot be assessed from the video, and the video avoids the
test.** Every bar discussed is historical. The live right edge of the pane
sits under the webcam overlay. No bar is watched forming. The only way to
judge repainting is to compare values plotted live against values after
reload, and the video shows neither. Treat it as **unknown**. For any script
that splits volume from lower-timeframe or intrabar data, a
`request.security_lower_tf`-style build is exactly where historical and
realtime values can differ.

**Performance claims: one, unevidenced.** 05:01: *"combined with simple price
actions like this to find a very, very high accurate trade."* There is no win
rate, no backtest, no count of signals, no losing example, and no costs.
05:15: *"this is just one example, and I will make more."* That is the whole
evidence base.

**Commercial payload (verified: description + redirect).** The description
link `zeiier.com/fn9b22s` 302-redirects to
`zeiierman.com/?utm_source=youtube&utm_medium=social&utm_content=vid-this-order-flow-indicator-is-seriously-overpowered`.
That is the vendor's own shop, with a per-video tracking tag. There are no
third-party affiliate codes. The on-screen call to action is only
*"Make sure to follow"* (05:22). Price and access tier (free, paid or
invite-only) are not stated in the video or the description. The pane's
`(Zeiierman)` tag and "our Buy & Sell Order indicator" (00:01) make the
presenter the seller. Disclaimer: *"Only for educational and entertainment
purposes."*

### Gemini misreads (worth recording)

Every identity field Gemini read off this chart was invented. It gave the
pane author tag four different ways: `[Deltonex]` (wide pass),
`[QuantSecret]` (00:00–01:50), `[QuantVue]` (01:50–03:40) and `[Darkmatter]`
(03:40–05:26). The frames read `(Zeiierman)`. It gave the dates as
**Aug–Sep 2023**, the price as **1,928–1,950**, and the timeframe once as
**1m**. The frames read Sep 2026, about 4,240–4,400, and 15m. It reported the
pane scale as `500 / 0 / −500`, apparently from the spoken "500". It gave the
position tool as `Target 14.165 / Stop 4.885 / R:R 2.90`. That triple is
internally consistent (14.165/4.885 = 2.900) but wrong. The tool reads
28.414 / 7.745 / 3.67. **These were derived numbers that passed arithmetic by
construction**, the Cherry Bomb failure again. The narration transcripts
matched what the frames and the description chapters imply.

## How it compares to the order-flow method in the corpus

The corpus's order-flow method is Carmine Rosato's
([playlist synthesis](../../playlists/orderflow-series-PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ.md),
[eJZhX6Xz4cU](../eJZhX6Xz4cU/CARD.md), [tgQC7Dpcc8A](../tgQC7Dpcc8A/CARD.md),
the InvestiTrade course). Tom Vorwald's volume/footprint cards
([vl01TiVTuoQ](../vl01TiVTuoQ/CARD.md), [RwQBdF9TSvc](../RwQBdF9TSvc/CARD.md))
teach the same thing. It is read from **exchange-traded futures (ES) on
real trade data**: Time & Sales aggressor side, footprint bid×ask per price,
delta = ask − bid, DOM, and Bookmap. Its signals are *specific events at a
price*: absorption, trapped participants, and failure of follow-through at a
level. This indicator has none of those inputs. It works on an OTC spot
feed. It reduces "order flow" to one bar colour per candle, and uses it as a
trend filter ("green = look for longs"). The only overlap is vocabulary
("order flow", "delta", "institutions"). The entry itself is a
liquidity-sweep-and-reclaim of a higher low. That is price action out of the
SMC cards (e.g. Smart Money Decode X), not an order-flow read.

Against the corpus's other indicator videos, it is weaker than AlgoTrade Pro
([UL5QOCSKnU0](../UL5QOCSKnU0/CARD.md)). That video was also a funnel, but it
published falsifiable tables (8,065 trades, PF 1.05) that could be checked
and broken. Here there is nothing to check. Like fvid
([sASTlqfPg-8](../sASTlqfPg-8/CARD.md)), the title's claim ("order flow")
does not survive contact with the content.

## Grade

**Clarity: C.** The entry, stop and target rules are stated plainly (04:16–04:32)
and the trade is legible. What the indicator computes, its settings, and how
often the rule works are all absent.

**Alignment to the corpus: D.** It borrows the order-flow vocabulary without
the order-flow data, on an instrument where that data does not exist.

**Net.** Not worth buying or testing on the strength of this video. If Steve
wants the idea, "trade in the direction of sustained aggressor delta, enter
on a failed sweep", he can build it from real ES footprint/CVD data in the
corpus's own tooling. It would then be testable against the Databento tape.

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-25 — credibility assessment (bead dr-w5l).** Wide pass at defaults
  (runs/20260925-133309, 30,136 prompt tokens) plus three verbatim zooms
  covering the whole video (133334, 133347, 133359). Frames at 0.25–0.5 fps
  over 00:00–00:30, 01:40–02:00, 04:10–04:40 and 04:50–05:26, viewed directly
  with crops of the header, position tool, price axis and pane. The
  description came via yt-dlp and the shop link was resolved by redirect.
  Verified the chart identity, live recording, trade levels and R:R (frames
  plus arithmetic), and the hindsight (`Closed PnL` on the tool, four-day
  gap). Overturned every chart-identity field and the position-tool numbers
  in all four Gemini runs. Verdict: low credibility; no performance evidence;
  what it computes is undisclosed but constrained to a price/tick-volume
  proxy by the OANDA feed.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **Zeiierman records on a live TradingView chart with a webcam bubble over
  the bottom-right corner**, which is exactly where the pane's live bar sits.
  Repainting cannot be seen through it. Ask for a different video (or the
  script's source) if repainting matters.
- **Read the data feed in the chart header before reading any "order flow"
  claim.** `· OANDA` (or any FX/CFD feed) means no aggressor-side data exists.
  Every "delta" on it is a proxy.
- **Every identity field Gemini read on this channel was invented.** That
  covers the author tag, dates, price level, timeframe and position-tool
  numbers. Frame the header and the tool first; they are cheap and decide the
  rest.
- The description carries Zeiierman's own chapter list and a
  `zeiier.com/<code>` short link that resolves to the vendor shop with a
  per-video `utm_content` tag.

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
- 20260925-133309 [full] gemini-flash-latest (tok 30136/1057) — Q: This video promotes a TradingView order-flow indicator. Report: (1) the indicato… — runs/20260925-133309/
- 20260925-133334 [00:00-01:50] gemini-flash-latest (tok 10364/2241) — Q: Transcribe the spoken narration in this window VERBATIM with timestamps (every s… — runs/20260925-133334/
- 20260925-133347 [01:50-03:40] gemini-flash-latest (tok 10364/1652) — Q: Transcribe the spoken narration in this window VERBATIM with timestamps (every s… — runs/20260925-133347/
- 20260925-133359 [03:40-05:26] gemini-flash-latest (tok 9994/1429) — Q: Transcribe the spoken narration in this window VERBATIM with timestamps (every s… — runs/20260925-133359/
