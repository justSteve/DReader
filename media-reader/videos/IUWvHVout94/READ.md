# Read: Read Liquidity Like a Pro: The 3 Step Strategy That Actually Works

> **The corpus's clearest account of why stops get taken without anyone hunting them: an execution algorithm that simply stops bidding for a few minutes, and a three-step sweep strategy built on top of it that never says where to enter.**

- **Channel:** Trading Notes · **Uploaded:** 2026-09-04 · **Duration:** 16:08
- **Card:** [CARD.md](CARD.md) · **Watch:** https://www.youtube.com/watch?v=IUWvHVout94

## In brief

The presenter opens with a sentence he credits to an unnamed physicist turned futures trader: nobody is hunting your stops. His explanation is the good part of the video. Liquidity is resting orders, and the two biggest clusters of them are stop losses and stop entries, stacked above every obvious high and below every obvious low. Any tool that produces predictable behaviour produces predictable liquidity. An institution filling a large buy order does not attack those clusters; its algorithm pauses its own bid, price sags into the stops, and it resumes buying at a discount. Harvesting, not predation. Iceberg orders then reload at the level for hours.

On that mechanism he builds a strategy: find an obvious pool, wait for a sweep that gets rejected, drop a timeframe and enter on the pullback after structure shifts. Stop beyond the sweep, target the pool on the other side. Invalidation is stated three times; the entry price is never stated once.

## The argument

The video is two things stapled together. The first six minutes explain liquidity better than most of the corpus explains anything. The rest is a strategy that inherits the explanation's confidence without its precision.

The explanation runs like this. A stop loss on a short is a buy order; a stop on a long is a sell order. Breakout traders add a second layer of the same orders at the same places. So above every obvious high sit two layers of buying, the trapped sellers' stops and the breakout buyers' entries, and below every obvious low the mirror image. The clusters form above equal highs, below equal lows, along clean trendlines and at round numbers, and he compresses it into one line: any tool that produces predictable behaviour produces predictable liquidity.

The piece he says nobody tells you is that liquidity at any instant is close to zero; it exists over time. When a cluster of stops fires at once, a wave of market orders hits a book that is momentarily empty, which is why price explodes through these levels rather than walking through them. This is [Carmine Rosato's auction premise](../QaNPAaEnB5E/CARD.md) seen from the stop-holder's side: a fired stop is an aggressive order arriving where the passive side has just thinned.

Who is pulling the trigger? A fund hands a large order to an execution algorithm graded on slippage. That algorithm has been buying for hours and can see the sell stops under the session low. So it stops buying. It sells nothing, attacks nothing; without its bid, price drips into the stops, and it resumes buying lower. This is the middle position in the corpus's three-way argument about stop-hunting. The [Vorwald podcast](../RwQBdF9TSvc/CARD.md) calls stop-hunting a myth because only single-digit prints trade below chart lows, yet concedes positions get closed there as a normal principle; Trading Notes agrees on both counts, denying the hunter while affirming the harvest, and differs only in thinking the harvest is tradeable. [Carmine's premise episode](../0QlGCz6U_1g/CARD.md) is the opposite pole, where the hunt is real and is exactly where he buys at wholesale.

The second mechanism is the iceberg: an institution shows only the tip of its order, a few hundred contracts, and the rest reloads at the level, which is why price drifts one way for hours after a flush. It is the second independent naming of the iceberg in the corpus, with [the Vorwald heatmap video](../Vd83oo_geMk/CARD.md); Carmine calls the same thing absorption in [his series summary](../00QtD-RosLg/CARD.md). His "few hundred contracts" sits beside the Vorwald channel's threshold for a large standalone order on the S&P, over 250 to 300, and the [325-contract ask](../vl01TiVTuoQ/CARD.md) it showed live.

He then concedes what few strategy videos do: not every failed breakout is any of this. The chart shows the effect, never the reason.

The strategy. Step one, a pool so obvious a five-year-old could spot it, equal highs or lows respected two or three times, the Asian session extremes, yesterday's high and low, confirmed by the market: no respect and move away, no confirmed pool. That is [Carmine's support-and-resistance rule](../5qBo04SMUFc/CARD.md) with a coarser sensor, confirmation from price rather than from order flow. Step two, wait for the sweep and tell it from a real breakout: a body at least twice the previous candle, closing far beyond with a small wick and a volume spike, is a train, stand aside; a poke through that gets slammed back inside is the sweep. Carmine's [first-test fade](../w7tvJCuZAq8/CARD.md) makes the same call on the tape, aggressive volume with no follow-through, and needs no candle ratio. Step three, drop a timeframe, wait for higher highs and higher lows to break into a lower low, enter on the pullback. Stop beyond the sweep's extreme, target the opposite pool.

Sweep first, structure shift after, as separate events: exactly what the [Smart Money Decode X structure video](../dAlP8UZXT48/CARD.md) insists on when it says a one-to-two-candle snap-back is a sweep and not a change of character. Where it is weaker is precision: no pullback depth, no trigger candle, no timeframe pair, so two traders following it would not enter at the same price. On whether the break needs a candle close the strategy section is silent, and the corpus is split: SMDX and the Vorwald channel want a close, [Carmine](../7facFfjQ0UE/CARD.md) argues that waiting for one turns a two-point stop into a seven-point one. He does eventually claim his rule is on closes, but only while demonstrating a paid indicator that works that way.

The two chart illustrations that follow are on other index futures and are cut here. Then an affiliate demo of the Flux Charts toolkit that [AlgoTrade Pro](../UL5QOCSKnU0/CARD.md) promoted the same week, and three closing mistakes, the third of which is the whole method: sweep plus shift plus pullback, all three or nothing.

## In his words

**The sentence that started it** *(00:17)*

> "I ran into an interview with a particle physicist turned eight-figure futures trader, a man who has been beating the market for 30 years. And one sentence stopped me cold. 'Nobody is hunting your stops.' [...] In this video, I'm giving you everything I found. The truth about hunting stops and a complete three-step strategy to ride these moves instead of feeding them."

> **Editor —** The physicist is never named, on screen or in audio. Every claim in the mechanism section is sourced to him, so the video's authority rests on someone we cannot check. The mechanism stands or falls on its own logic.

**What liquidity is** *(01:02)*

> "In practical terms, liquidity is resting orders. Orders that are already sitting in the market waiting to be triggered. And the biggest clusters of resting orders on any chart come from two sources. Source number one, stop losses. Think about what a stop loss really is. If you are short from a resistance level, your stop sits above that resistance. And when it triggers, it does not just close your trade, it buys. A stop loss on a short position is a buy order. A stop loss on a long position is a sell order. Now, multiply that by thousands of traders who all learned the same lesson. Sell resistance with a stop above the highs. Buy support with a stop below the lows.
>
> Source number two, stop entries. Breakout traders place buy stops above resistance because they want to be triggered into the move if the level breaks. And they place sell stops below support for the same reason. So, above every obvious high, you have two layers of buy orders stacked on top of each other. The stops of the trapped sellers, plus the entries of the breakout buyers. Below every obvious low, the exact mirror image."

**Where the clusters form** *(02:12)*

> "Above equal highs, below equal lows, along clean trend lines, and around big round numbers. Because human beings love placing orders at 100.00, and almost never at 99.17. Here is the general law. Any tool that produces predictable behavior produces predictable liquidity."

> **Editor —** The best line in the video, and the one the rest of the corpus keeps circling. The Smart Money Decode X series says the same thing as "your breakout entry is their exit liquidity"; Carmine says retail is the bait fish. This is the version that explains the mechanism rather than assigning a villain.

**Liquidity is close to zero at any instant** *(02:36)*

> "The liquidity of the market at any given instant is close to zero. Liquidity exists over time, not in a single moment. Picture a stadium with 60,000 people and only one gate open. Over the whole evening, everyone gets out just fine. But, if everybody pushes toward the gate in the same second, you get a crush. That is exactly what happens when a cluster of stops fires all at once. A wave of market orders slams into an order book that, in that precise instant, is almost empty. And that is why price does not walk through these levels. It explodes through them."

> **Editor —** This is [Carmine's auction premise](../QaNPAaEnB5E/CARD.md) from the other side of the book: aggressive orders consuming passive ones, and the passive side momentarily gone. The [Vorwald podcast](../RwQBdF9TSvc/CARD.md) holds the corpus's only numbers on what the book actually does in a crisis; this is the intuition those numbers describe.

**Who is pulling the trigger** *(03:17)*

> "Who is pulling the trigger? And this is where it gets interesting, because the answer is not what 90% of trading YouTubers tell you. Picture this. A pension fund decides to buy 2 million shares of a stock, or 5,000 contracts of an index future. They do not care about your stop loss. They care about one thing only, getting filled at the best possible average price. So, they hand the order to an execution algorithm, and that algorithm gets graded on one metric, slippage. How close was the final average price to the price when the order started?
>
> Now, put yourself in the shoes of that algorithm. You have been buying steadily for 2 hours. Your own buying is what has been holding the price up, and you can see, just like everyone else can, that there is an obvious cluster of sell stops resting just below the session low. What do you do? You simply stop buying for a few minutes. That is it. You do not sell anything. You do not attack anything. You just step aside. Without your bid, price sags, drips into the cluster, the sell stops fire, weak hands panic, and now you switch your buying back on and load up at a discount.
>
> Watch that again, because it changes everything. Nobody hunted your stop. An algorithm knew your stop was there because you placed it exactly where everybody places it, and it simply paused until the market delivered the shares at a better price. This is not predation. It is harvesting."

> **Editor —** Three sources, one question. The [Vorwald podcast](../RwQBdF9TSvc/CARD.md) says stop-hunting is a myth because the prints below chart lows are single-digit, then concedes positions have to be closed there as a normal principle. Trading Notes agrees with both halves and adds the mechanism: nobody has to sell into the lows if the buyer simply stops bidding. [Carmine](../0QlGCz6U_1g/CARD.md) calls the same event a stop hunt and buys inside it. The disagreement is over whether anyone is steering and whether it is tradeable, not over whether the stops get filled. Note also what the algorithm story does not need: any size trading below the low. That is precisely the Vorwald evidence, and this account is consistent with it.

**Iceberg orders** *(04:51)*

> "And there is a second mechanism stacked on top of it. Iceberg orders. When an institution buys, you only ever see the tip of the order book, a few hundred contracts. Underneath sits the rest of the iceberg, reloading at the same level again and again. That is why, after the flush, price does not simply bounce. It drifts in one direction for hours. The whale is still feeding."

> **Editor —** The second independent naming of the iceberg in the corpus, with [the Vorwald heatmap video](../Vd83oo_geMk/CARD.md). Carmine's absorption in [his series summary](../00QtD-RosLg/CARD.md) is the same mechanism read on the footprint: heavy aggression that fails to move price. His "few hundred contracts" for the visible tip is the same order of size the Vorwald channel calls large on the S&P, over 250 to 300 contracts standing alone, and the [325-contract ask](../vl01TiVTuoQ/CARD.md) it showed the market run to.

**The chart shows the effect, never the reason** *(05:18)*

> "One last dose of honesty before we move on. Not every failed breakout is even this. Sometimes a breakout fails simply because there was no follow-through interest. Sometimes a market maker is just covering risk. Sometimes a big fund is moving money around and does not even look at your chart. The chart shows you the effect, never the reason. Remember this, because it explains why this strategy, like every strategy, will sometimes fail even when you do everything right. So, if there is a whale in the water and you cannot fight it, there is only one intelligent thing left to do. You do what the remora fish does with the shark. You attach yourself and you ride."

**Step one, identify the pool** *(06:08)*

> "You are only interested in liquidity pools so obvious that a five-year-old could spot them. Equal highs or equal lows that have been respected two or three times. The high and low of the Asian session, yesterday's high and low, a level the whole market is watching. And here is the golden rule. You do not predict where liquidity should be. Let the market show you where it is. When price approaches an old high, respects it, and moves away, the market has just told you in plain language that orders are stacking above that high. No respect and move away, no confirmed pool."

> **Editor —** "Let the market show you" is [Carmine's support-and-resistance position](../5qBo04SMUFc/CARD.md) with a different instrument: a level is only real when the market confirms it. Carmine reads the confirmation in the order flow, aggression exhausting into passive size; this video takes it from price respecting the level. Same principle, coarser sensor.

**Step two, wait for the sweep and make sure it is a sweep** *(06:48)*

> "This is where most traders die, so pay attention. When price finally breaks your level, there are two possible animals in front of you and they look similar for about one candle. Animal number one is the real breakout, a momentum candle with a body at least two times the previous candle closing far beyond the level with a small wick and a clear spike in volume. If you see that, stand aside. That is not a trap, that is a train.
>
> Animal number two is the sweep. Price pokes through the level, triggers the stops, and gets slammed back inside leaving a wick or closing weakly right back within the range. That rejection is your signal that the flush just happened and the whale just finished its shopping."

> **Editor —** Carmine's [first-test fade](../w7tvJCuZAq8/CARD.md) is the same discrimination made in the tape: aggressive volume at the break with no follow-through is the sweep, follow-through is the train. He gives no candle-body ratio and would not; his classifier is the footprint, not the bar. The two-times body and the volume spike here are the only quantitative rules in the video, and "clear spike" is never given a threshold.

**Step three, enter on confirmation** *(07:38)*

> "The sweep alone is only half a signal. After the sweep, drop to your lower time frame and wait for the structure to actually shift. If the market swept the highs and you want to short, you need to see the sequence of higher highs and higher lows break into a lower low. That break is the market confirming that control has changed hands. Then you enter on the pullback. You place your stop loss beyond the extreme of the sweep and you target the liquidity pool on the opposite side of the range. Swept the highs, target the lows. Swept the lows, target the highs. Internal liquidity gets you in. External liquidity gets you out.
>
> And one iron rule to glue everything together. If the level has not been swept, there is no trade. It does not matter how beautiful the setup looks. No sweep, no trade. No exceptions."

> **Editor —** Sweep first, structure shift after, as two separate events: the same ordering the [Smart Money Decode X structure video](../dAlP8UZXT48/CARD.md) enforces when it says a one-to-two-candle snap-back is a sweep and not a change of character. What is missing is everything that would make it reproducible. "Enter on the pullback" has no depth, no trigger, and "your lower time frame" has no value. Whether the lower low needs a candle close is not said here, and the corpus disagrees on it: SMDX and the Vorwald channel require a close, [Carmine](../7facFfjQ0UE/CARD.md) argues that waiting for one moves a two-point stop to seven. The two chart illustrations that follow are on other index futures and are cut here for scope; they show no prices, and the on-screen label for their third step reads "ENTRY ON SWEEP", with the entry narrated as going right after the sweep. The example does not visibly wait for the shift and pullback the rule requires.

**"Exactly like our rule"** *(12:46)*

> "Turn on market structures. The toolkit labels every break of structure and every change of character automatically, and it does it on candle closes, exactly like our rule."

> **Editor —** The one place the video says the structure shift is judged on closes, and it arrives inside the paid-indicator demo, describing the tool's behaviour rather than restating the rule. Take it as his intent, not as a stated step. The demo itself is cut: it is an affiliate walkthrough of the Flux Charts toolkit that [AlgoTrade Pro](../UL5QOCSKnU0/CARD.md) was promoting the same week, and the presenter says on camera that he earns a commission.

**Three mistakes** *(14:04)*

> "Mistake number one, parking your stop loss in the obvious place. One tick below the support, exactly at the round number, right under the trend line. You are literally donating your order to the cluster. Give your stop breathing room beyond the zone. Place it at ugly, asymmetric prices, and if you want to go full physicist about it, avoid prices ending in zero or five altogether.
>
> Mistake number two, selling equal highs and buying equal lows directly. I know it feels safe. It is the opposite of safe. When you short a double top with your stop above the highs, you are placing your order exactly inside the pool that the market is most likely to raid before the move. If a level is obvious enough to attract you, it is obvious enough to get swept. Trade the sweep of the level, not the level itself.
>
> Mistake number three, treating the sweep alone as an entry signal. The sweep is half a signal. Without the structure shift, you have zero evidence that control actually changed hands, and sooner or later, you will buy a flush that turns out to be the start of a real breakdown. Sweep plus shift plus pullback. All three, every time, or nothing."

> **Editor —** Mistake two is the practical consequence of the whole first half, and it is where this video and [Carmine's premise episode](../0QlGCz6U_1g/CARD.md) converge from opposite directions: do not sell the double top, sell the failed run above it. Carmine gets there through the stop hunt he believes in; Trading Notes gets there through the harvest it says nobody is running.

**Process over result** *(15:29)*

> "And one final gift from our physicist, maybe the most valuable sentence in this entire video. It is always better to follow a good process and get a bad result than to follow a bad process and get a good result. Because a bad process that gets rewarded teaches you the wrong lesson, and unlearning it is 10 times harder than learning."
