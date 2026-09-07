# Read: BEST Zero-Lag Indicator On TradingView? I Tested It 8,000 Times & It's FREE

> **The only video in the corpus that puts a number on a signal: a free trend-flip indicator run through 8,065 trades, a five-minute profit factor of 1.05 before any cost, and on ES the costs come to nearly twice the edge.**

- **Channel:** AlgoTrade Pro · **Uploaded:** 2026-09-04 · **Duration:** 7:40
- **Card:** [CARD.md](CARD.md) · **Watch:** https://www.youtube.com/watch?v=UL5QOCSKnU0

## In brief

A presenter who calls himself ATP takes a free TradingView indicator, Zero Lag Trend Signals by AlgoAlpha, wires it into his own backtesting product and reports what it did across five markets and four timeframes. The rules are stated precisely enough to implement: buy a bullish flip, sell a bearish one, stop at the most recent swing, take half off at one-to-one, move the stop to breakeven and trail the rest. The spreadsheet he shows adds up.

What it says, once you read it instead of listening to him, is that the five-minute version wins 48.98% of the time with a profit factor of 1.05, draws down 75%, and was tested with no commission, spread or slippage. Priced against real ES friction on the stop rule he specifies, that edge is under water before the first trade. The thirty-minute and hourly versions survive costs and fail on drawdown. Nothing here is tradeable, but everything is checkable, which makes it the corpus's benchmark for what "a free indicator with a 49% win rate" is worth.

## The argument

He opens with a claim every trader has felt: indicators lag, and by the time a moving average turns, the move is over. The remedy is a zero-lag EMA with ATR volatility bands around it. A close above the upper band flips the trend bullish; a close below the lower band flips it bearish; an arrow prints. Smaller arrows mark continuation entries inside the trend. Two settings matter, the EMA length and the band multiplier, and he keeps the defaults of 70 and 1.2 "so results stay fair and realistic".

> **Editor —** A signal that requires a close beyond a band is, by construction, at least one bar late, and the spreadsheet confirms the engine executed on bar close. "Zero lag" describes the smoothing, not the trade. This is [Carmine Rosato's](../7facFfjQ0UE/CARD.md) quarrel with the whole indicator school: waiting for a five-minute close to validate a thesis costs you the first ten or twenty points of the move, and confirmation belongs in the live tape, not the clock. This video does not answer him; it measures what the clock-based version earns.

The test rules are the strongest passage: entries on flips, stops at the most recent swing low or high, and a hybrid exit, half closed at one-to-one, stop to breakeven, the remainder trailed. It is rare in this corpus to hear an exit fully specified. Set it beside the one trade the Vorwald channel takes on camera, the [pre-market DAX short](../yWO8hVpRXeY/CARD.md) where the presenter refuses to move his stop to zero and walks it behind structure instead. Breakeven is an account number; that trader's stops are auction facts. Opposite philosophies of exit, and only this one has a number attached.

The engine is his own product, the Signal Engine, which reads any indicator's events off the chart without source code and hands them to TradingView's Strategy Tester. It is also what the channel sells, and the test inherits every default of that tester, the most consequential being zero cost.

The results as he reads them: 125% net profit at a win rate close to 49% on five minutes, "not the strongest headline number"; over 300% at 50% on thirty minutes with every market profitable; 290% at 51% on the hourly; fewer trades and an average result on the daily. The S&P 500 is named as one of the two five-minute winners; two of the five markets lost money there.

Now the spreadsheet. It is internally consistent to four decimal places, so the numbers are real and can be interrogated. Net profit divided by average profit per year forces the five-minute test to exactly two years, whatever the "All Available Data Since 2020" banner above it says; the other tables cover different spans, so the rows are not comparable. The Sharpe ratio of 4.19 sits beside a 75.42% maximum drawdown and an average drawdown of 28.30%, which no return series with 14.48% annualised volatility can produce; treat every Sharpe here as void. And the profit factor of 1.05 on 2,440 trades means an edge of $51.31 per trade on $2,000 risked, about 0.026 R, gross.

That gross qualifier is where the corpus enters. The Vorwald channel's [statistics video](../NkQeOVDTAec/CARD.md) says you need 200 to 300 trades before a figure means anything. This test clears that bar many times over on the intraday tables, which is why its result is damning rather than noisy: the five-minute edge is not an artefact of sample size but of costs. Our own ES tick data puts the median five-minute swing stop at 7.00 points and round-turn friction at $17 a contract, so the cost of one trade is 0.0486 R against an edge of 0.0257 R. The stop would need to be 13.2 points for the strategy merely to break even; 80% of five-minute setups are negative-expectancy before entry. On thirty-minute bars the swing stop widens to 20.25 points and the edge is roughly three times the friction, so that variant survives costs and dies instead on a 62.90% drawdown at 2% risk. This is the friction figure the corpus now uses against the Vorwald channel's [one-minute scalping video](../zAwEX_tRUfE/CARD.md) and its [80 to 90% win-rate claim](../uFxYcpiaOpw/CARD.md).

Two cautions for an S&P reader. The tested instrument is SPX500, a CFD, not ES: different spread, tick, roll and session, and a CFD spread on a seven-point stop is worse than the ES figure, not better. And the S&P's own rows on the spreadsheet are not in the card; the five-minute row is given below, marked as such.

His pro tip, a 200 EMA baseline filter so longs are taken only above it and shorts below, arrives after the results and changes the tested rules; he asserts a win-rate improvement and shows no table for it. The indicator then goes into his site's ranking table, which is also the product being sold, and the description carries Flux Charts, the sponsor [Trading Notes](../IUWvHVout94/CARD.md) shares the same week.

## In his words

**Every indicator lags** *(00:00)*

Every indicator on TradingView has the same fatal flaw: lag. By the time it gives you a signal, the move is already over. But recently, a member of our Discord community found a new indicator that fixes exactly that. And honestly, after putting it on the chart, I understood why. Somehow, it gives signals with amazing accuracy. So, in today's video, I'm going to show you exactly how this free indicator works with the best settings. And on top of that, I'm going to test it on more than 8,000 trades to show you the real results it actually delivers.

Look at this. This is a basic indicator all of you have probably used before. Price reverses at this moment, but the signal only comes a few candles later. Now, look at the zero lag indicator on the exact same chart. Same reversal, but the signal comes with zero delay. That's the difference between catching a move and chasing it.

> **Editor —** "8,000" is trades, not test runs, and the four tables sum to 8,065. Note also "the best settings" here against "keeping the defaults" two minutes later; the video says both.

**How the indicator works** *(01:04)*

This is the indicator right here. It's called Zero Lag Trend Signals, built by AlgoAlpha. And right away, you can see that it's not just a line on the chart, it's a full system. At its core, it uses a zero lag EMA. So, instead of being built from past data like a standard moving average, it follows price much closer and reacts to trend shifts instantly. Then, around that line, it plots volatility bands built using the ATR. When price closes above the upper band, the trend flips bullish. And when it closes below the lower band, it flips bearish. And every time that happens, a clean arrow prints directly on your chart.

Besides the big flip arrows, you'll also notice smaller arrows appearing along the trend itself. These are separate entry signals marking additional bullish or bearish opportunities while the major trend is still active. And for the settings, the EMA length controls sensitivity and the band multiplier controls how far price needs to move to trigger a flip. For today's test, we are keeping the defaults so results stay fair and realistic.

> **Editor —** The defaults on screen are Length 70 and Band Multiplier 1.2. On five-minute bars a length of 70 is nearly six hours of warm-up, which is what makes this indicator impossible to run on most of our own ES corpus, where the bulk of the days are two-hour afternoon fragments. Keeping the defaults does mean the parameters were not fitted to this data, which is to his credit; it does not mean they were not fitted to something.

**The rules** *(02:20)*

Now, let's define how we are going to trade these signals. For entries, we'll keep it simple. Long trades on bullish flips, short trades on bearish ones. For stop losses, we'll use the most recent swing low or swing high. And for take profits, we are using a hybrid system. We'll close 50% of the position at a one to one risk to reward ratio, move the stop loss to break even, and let the remaining 50% run with a trailing stop loss. This way, we lock in partial profits early, but we still let the strategy capture the bigger trend moves when they happen.

> **Editor —** The clearest exit specification in the corpus, and the one our ES cost test priced, since the stop distance is what the friction is measured against. One unresolved wrinkle: the spreadsheet's settings column at 04:41 also carries an ATR-based stop-and-target line that the narration never mentions, in a row the transcription reports as partly obscured. If the trades were generated off that rather than off the swing, the stop distances differ and so does the cost arithmetic. The video does not say which rule the engine actually used.

**The engine** *(02:59)*

But of course, testing all of this manually will take forever. So, I will use the Signal Engine. I already have both the Zero Lag Trend Signals indicator and the Signal Engine loaded together on the chart. And the powerful part is this: I don't need access to the source code, I don't need to build a strategy manually, and it doesn't matter if this is a free indicator or not. As long as it is on the chart, I can test it. [...] And instantly, all the trades appear automatically on the chart including entries, stop losses, and take profits. Then, down here inside the Strategy Tester tab, we get real historical performance data like win rate, drawdown, net profit, and much more. And the craziest part is this: if I change the indicator settings, the entire strategy updates automatically. If I switch [...] to another market, the backtest recalculates instantly. And if I change the time frame, same thing. Everything updates in seconds.

> **Editor —** Two things the tester inherits and he does not mention. First, it executes on bar close, and with a target at one-to-one and a stop in the same bar it cannot know which was hit first; that ambiguity flatters exactly this kind of hybrid exit. Second, it charges nothing per trade unless told to, and a dedicated pass over the settings found no commission, spread or slippage row anywhere. Every figure that follows is gross.

**The results** *(04:39)*

Starting with a 5-minute time frame, the strategy delivered 125% net profit with a win rate close to 49%. Not the strongest headline number. The S&P [...] got strong results, but [...] two markets were deep in the red. But on the 30-minute chart, everything changed. Net profit jumped to more than 300% with a solid 50% win rate. [...] And this was the biggest surprise of the entire test, because all assets finished profitable and the equity curve looks very stable. Moving on to the 1-hour chart, results stayed strong. 290% net profit, a 51% win rate with a strong equity curve, and once again, all assets were profitable. And finally, on the daily chart, the strategy delivered fewer trades and had an average performance.

> **Editor —** The spreadsheet behind this passage, five-minute table: 2,440 trades, 48.98% win rate, profit factor 1.05, net 125.21%, maximum drawdown 75.42%. Divide the net by the average per year and the test is exactly 2.000 years long, whatever the "Since 2020" banner says; the thirty-minute and hourly tables run six years and the daily five, so the rows are not on a common footing. The Sharpe of 4.19 is arithmetically consistent with its own inputs and physically impossible beside that drawdown. The S&P row on the five-minute sheet, transcribed twice with the same reading but not carried in the card and not frame-verified: net 99.46%, maximum drawdown 23.77%, win rate 49.08%, 491 trades. Per-market figures for the other four symbols are omitted here by scope. "All assets finished profitable" on the longer timeframes is true as far as the tables go; the daily table is 222 trades across five markets, a few dozen each, below the sample the Vorwald channel says you need before a figure means anything.

**The verdict and the pro tip** *(05:42)*

So, did we just find the best zero lag indicator on TradingView? For a free indicator, the results generally surprised us, especially on the 30-minute and 1-hour time frames. It's one of the best indicators we have tested on this channel so far. And here is a pro tip. If you want to push the performance even further, you can easily add a baseline filter like a 200 EMA, only taking longs above it and shorts below. And you'll see your win rate jump by 3 to 5%. Inside the Signal Engine, you can do that as well. You just enable the baseline section, select your moving average and length, and instantly only the trades aligned with a major trend get taken. [...] Now, as usual, we are going to place this indicator inside our official indicators ranking table, which you can consult completely free on our website.

> **Editor —** The 3 to 5% is his figure, unverified: no table in the video carries it, and the filter was not part of the test that produced the tables. "Generally" is the caption's word; "genuinely" is the likelier one, left as heard. The ranking table is the channel's own leaderboard, and the leaderboard is what the subscription sells.
