# Read: STOP Using Candlestick Charts, Use This Instead

> **The footprint chart as Carmine actually uses it: completed transactions per price, collapsed to delta, read for one thing, aggression that fails to move price. The 3 October 2024 long is the worked example.**

- **Channel:** Carmine Rosato, "Trading Orderflow Series" ep. 2 · **Uploaded:** 2024-10-18 · **Duration:** 24:53
- **Card:** [CARD.md](CARD.md) · **Watch:** https://www.youtube.com/watch?v=eJZhX6Xz4cU

## In brief

A candlestick tells you where price went, not what it cost to get there, and
Carmine argues the cost is the only intraday question worth asking. A lower
wick is not evidence of buying; it is a question about who put it there, real
buyers or sellers who ran out of push, and the two cases have opposite
futures.

His answer is the footprint: Time and Sales aggregated per price for each bar,
split into market sells that hit the bid and market buys that lift the ask,
then collapsed into one number, delta. He shows his three-column Sierra Chart
layout and the read the strategy rests on: when the most aggressive selling of
the day prints at the low and price does not go lower, someone is absorbing it
and the sellers are trapped. That read produced the 3 October 2024 long, a
delta of −1171 at the session low, $21,750 on $2,250 of risk.

It is also the episode where he is asked for a threshold and declines to give
one.

## The argument

He starts by reversing the usual causality. Charts do not move
price; price moves charts, and price moves because somebody placed an order.
Indicators, wicks and "ICT trading" all go into episode one's funnel; an order
comes out. The Vorwald channel opens from the same premise, order flow as who
is buying now and how aggressively ([vl01TiVTuoQ](../vl01TiVTuoQ/CARD.md)),
and neither cites the other.

The lower wick is the best early example. The wick is the question, not the
answer: strong buyers put it there and the rally probably continues, or
sellers failed to push lower and it probably does not. Smart Money Decode X's
candle-anatomy video ([oktlv1rOG9Q](../oktlv1rOG9Q/CARD.md)) rules a long
lower wick at key support a "powerful signal"; Carmine's point is that the
same wick has two possible authors and the candle cannot say which.

He concedes that resting volume can be spoofed and liquidity pulled, which is
why he avoids tools that can be faked. Time and Sales is his receipt: nothing
prints unless a transaction completed, and every completed transaction has an
aggressor hitting a passive side. The footprint is that receipt aggregated per
price per bar. His position on the book moves, though. Episode 3
([tgQC7Dpcc8A](../tgQC7Dpcc8A/CARD.md)) makes the DOM and the Bookmap heatmap
core tools, both built from the resting orders called spoofable here, and the
Vorwald channel ([Vd83oo_geMk](../Vd83oo_geMk/CARD.md)) draws the line in a
third place: the book is the true market, and professionals do not use
heatmaps. The whole corpus trusts the print; it splits on the book.

Delta is his noise filter, ask volume minus bid volume, and with it he drops
the bid × ask display. His own Sierra Chart layout is three columns on
20-tick, five-point range bars: total volume at price, shaded so heavy prices
read as fair value and thin ones as where the auction was cut off; delta at
price, blue positive and red negative; and a profile sized by total volume and
coloured by delta.

The read is aggression without result. Lots of aggressive participants at a
price with no follow-through is a sign of a possible reversal; heavy selling
that fails to lower price means a passive buyer is active, and with context
the sellers are trapped when price lifts. The Vorwald channel arrives at the
same mechanism on its own ([usho6UVLqkE](../usho6UVLqkE/CARD.md)), a buyer
repeatedly lifting a level and failing because a large seller is absorbing.

Asked whether he wants a delta above 100 or 500, "I don't have an answer to
that." He looks for outliers. No episode supplies a threshold; here the
absence is deliberate. The Vorwald channel's 250–300 contracts does not fill
it: that is the size of a resting ES order in the book, not an executed delta,
and that channel never gives a delta number either. Nobody in the corpus does.

The trade: −735 and −1171, the greatest negative deltas of the day, at the low
of the day, where an auction should have gone lower. It did not, "tons of
effort but no reward", and he bought where the selling came in. Episode 7's
Bookmap tooltip ([7facFfjQ0UE](../7facFfjQ0UE/CARD.md)) shows the same −1171
at 5739.75–5740. The series never shows a loser: seven journaled winners, no
hit rate, no sizing rule beyond thirty contracts. The only place in the corpus
where a hit rate and a risk-reward sit together is the Vorwald channel's
worked example ([NkQeOVDTAec](../NkQeOVDTAec/CARD.md)) at 50% averaging "maybe
a two".

The replay is the best teaching. Delta at the low builds from about average to
one print that adds roughly 900 contracts of selling, "and the market did not
move down." He is reading confirmation inside the bar, before it closes: the C
of episode 7's CLC rule, where waiting for the close turns a two-point stop
into seven. The Vorwald channel wants closes, not wicks
([Ly62G168MkQ](../Ly62G168MkQ/CARD.md)), and SMDX's change of character
([iPDi9_nzn-o](../iPDi9_nzn-o/CARD.md)) is a close below the last higher low.
Carmine acts mid-bar; both other schools wait for the bar to finish.

The second setup inverts the first. A breakout above 5733.5 looks strong on
candles; on the footprint the prints thin to almost nothing above the level, a
volume tail. Nobody wants it up there, so sellers must lower their prices.
Total volume alone, no delta required. The Vorwald channel's buying and
selling tails ([K8qtT2_axPo](../K8qtT2_axPo/CARD.md)) are the same shape drawn
in TPO time, and SMDX's "your breakout entry = their exit liquidity" is the
same trap named from the retail side. Carmine files "ICT trading" with
indicators; the Vorwald channel goes further and calls stop-hunting a retail
myth ([RwQBdF9TSvc](../RwQBdF9TSvc/CARD.md)).

Two caveats. The volume-tail example has no numbers spoken and no frames
pulled; the card leaves it unverified. And "nothing can be spoofed" is true of
prints, not motive: an aggressor can hit the bid to be seen, and he never
addresses that.

## In his words

**Price leads, the chart follows** *(01:43)*

> "Candlestick charts are great to show a picture of where the market has
> traded in the past, and it's great to show where the market is currently
> trading. But price doesn't move because of the candlestick charts. The
> candlestick charts simply move because of price. Price leads and the chart
> follows. The order flow and the volume and the transactions will provide the
> most important information, because this will give us a good feel of how
> other participants are perceiving the market at those specific prices."

**The lower wick is a question, not an answer** *(02:26)*

> "What a lot of traders are going to say is, hey, we see the market selling
> off, we see this lower wick down here. But Carmine, there's a lower wick, I
> could easily see that there's buying here because of a lower wick present in
> the market. And again, reading this information alone doesn't provide the
> information that's needed to understand why. Big question mark here: why did
> this lower wick form? If this lower wick formed by actual strong, true
> buyers, then it's very likely the market will eventually reverse and rally
> and continue moving much higher. However, if this lower wick right here got
> put in by a failure of sellers to move the market lower, then it's not as
> likely, or maybe a little bit of a lower probability, that the rally to the
> upside may not last. So yes, you can technically say that there is buying
> pressure by looking at a lower wick, but you don't know how strong, or the
> effort behind buyers or sellers that form these wicks."

> **Editor —** Smart Money Decode X's candle video rules a long lower wick at
> key support a "powerful signal". Carmine's point is that the identical wick
> has two possible authors with opposite implications, and the candle cannot
> tell you which. Keep his hedges: "very likely" for the buyer case, "a little
> bit of a lower probability" for the other. Neither is a certainty.

**The funnel** *(03:32)*

> "Like I talked about in episode one of this order flow series, we have water
> going into the funnel, we have stuff coming into it, and no matter what
> happens, at the end of the funnel water is going to come out. We could have
> indicators, we could have lower wicks, higher wicks, ICT trading,
> algorithmic trading. No matter what, somebody has to place an order. So
> reading this will provide the clearest, most organic and natural information
> to create a buy or sell thesis from these orders."

> **Editor —** Note where ICT lands: not rejected, filed with indicators as
> something upstream of an order. The Vorwald channel is harsher and calls
> stop-hunting a retail myth outright. Carmine subsumes the school; the German
> channel dismisses it.

**Who is in control at the level** *(04:01)*

> "Think about this. If you're looking to short the market at this resistance
> level, you have a level of supply, a level of resistance. If the market's
> coming up into this level of resistance, how can you truly tell who is in
> control of price? You cannot understand how strong sellers or how strong
> buyers are by strictly looking at a candlestick chart. […] The question mark
> is really how strong are participants, and how are other participants
> feeling about price trading here. This information cannot be found on a
> chart, but could only be found by using order flow data and reading the
> volume."

**The receipt** *(06:23)*

> "A lot of people always say, well, volume could be spoofed, or there's a lot
> of spoofing, or […] fake liquidity that gets pulled, and it may not really
> show true intention. And that's true, and this is why I don't focus on
> certain tools that can be easily faked or spoofed. A Time and Sales
> essentially shows the order book of completed transactions. Think of this as
> your receipt. The only way an item is going to show on your receipt is if
> you go to the cash register, complete the transaction, and buy or sell that
> good. […] If we bought something, we bought it from somebody who's selling
> something. If we sold something, we are selling it to somebody who bought
> that good."

> **Editor —** Hold this against episode 3, where the DOM and the Bookmap
> heatmap become core tools. Both display resting orders, the thing he here
> calls spoofable. The Vorwald channel says professionals do not rely on
> heatmaps and that the book itself is the true market. Everyone in this
> corpus trusts the print; they split on the book.

**The aggressor** *(07:10)*

> "In every transaction there's an aggressor. There's a participant who is
> very aggressive, that doesn't care what price they are paying, and then
> there's another participant who is very passive, that is a little more
> reserved, that cares about the price they pay for that good. When an
> aggressive participant hits a passive participant, this is when we have a
> completed transaction, which then gets reported on the receipt, which then,
> in the market's terms, is a Time and Sales. […] So if we see a red print on
> the Time and Sales for 130 contracts at 9:30 a.m. Eastern time at 5539, that
> means there was 130 aggressive sellers. These are the aggressors, hitting
> 130 passive buyers."

> **Editor —** The row on screen reads 09:30:11:072, 5539.25, 130, checked
> against frames; he rounds the price when he says it. SMDX's order-book video
> gives the same mechanics from a whiteboard: a market order consumes a
> resting limit and the fill is the new price.

**Inside the footprint** *(08:08)*

> "Now, leading this into footprint charts, this essentially shows an
> aggregated view of the Time and Sales based on the time frame that we are
> looking to trade at. […] On the left side of the footprint, highlighted in
> the red, we have market sell orders that hit the bid. So anything on the
> left side is a very aggressive seller present in the market, and a completed
> transaction. What we see on a footprint chart are completed transactions.
> Nothing can be spoofed, nothing can be faked. […] Anything on the right side,
> anything in the green, is aggressive market buy orders that hit the ask.
> […] No matter the time frame, a five-minute footprint, a one-minute
> footprint, maybe even a range footprint, we can see who is aggressive, we
> can see where a lot of the volume is being transacted, and we could see
> where there's less volume transacted, or where there's an imbalance present
> in the market."

**Intent** *(10:16)*

> "We are looking who is the aggressor in the market, because if you're
> aggressive, you were showing intention to be present, with an agenda to move
> the market up or down. […] If the market's rallying into a level of supply,
> what I want to see is how strong the sellers are here. If they're strong,
> then this is a bearish position that I would be looking to open. Well, if
> the market rallies up here and the sellers are not strong, which could only
> be spotted by reading the volume of the order flow, and I notice that
> sellers are a little weak, well then maybe I'm not interested in taking the
> market short here, despite it coming into my level of resistance or supply."

> **Editor —** This is the CLC rule two episodes before he names it. Location
> is the level; confirmation is the strength of sellers read on the footprint;
> a level without confirmation is a level he does not trade.

**Delta, and removing the noise** *(11:15)*

> "There's hundreds of different numbers that we could have on our footprint
> charts. Our objective is to remove the noise. And what I've seen a lot of
> traders do is they look at every single number at every single price. […]
> The first step in removing the noise is understanding the delta. If you ever
> hear me use the term delta, what this shows us is ask volume minus bid
> volume. So we are essentially subtracting all of the aggressive buyers by
> all of the aggressive sellers. If there is a positive delta, that means
> buyers are more aggressive, and if there's a negative delta, that means
> sellers are more aggressive. So in this example, up here at 5728.75, there
> was 51 aggressive buyers, because the buyers are on the right side, and only
> one aggressive seller. So 51 minus 1 equals 50. […] Now down here, 5724.50,
> we can see two contracts, two lots on the ask, so there's only two
> aggressive buyers, and 102 aggressive sellers. Ask volume, which is two,
> minus bid volume, which is 102, gives us a negative delta of minus 100.
> […] So we don't even need to look at an ask-versus-bid footprint chart,
> which is what a lot of traders are used to. We can just look at a delta
> footprint chart, because we are looking to remove the noise."

**His own footprint** *(13:33)*

> "This is my personal footprint chart. This is the only footprint chart that
> I use, and I use it on Sierra Charts. It's a custom footprint that I created
> myself. Column number one, which I've highlighted here in the middle, shows
> total volume at that specified price for that bar. […] We're not splitting
> it between bid or ask, we just know that there's 84 total volume. Now the
> reason I do this, and I have it shaded, is that in lower quantities of
> volume the gray is a little darker, and when the quantities are a little
> higher, the gray is a little lighter. […] I do this because when there's
> little volume, I could see where the auction essentially was cut off, and
> when there's a lot of volume, for example in the light gray, I know that
> there's fair value in the market."

*(14:35)*

> "Column number two, this is the most important column. Number two is delta
> at that specified price for that bar. Now I also want to mention that I
> personally use a 20-tick, or a five-point, range footprint chart, especially
> when I'm trading the S&P 500. […] So we have 84 total volume up here, and
> our delta is 84. So what that tells me is 84 was done on the ask and zero
> was done on the bid. […] Versus down here, we could see a 216 positive delta
> versus 366 total volume. What this tells me is there's 216 more aggressive
> buyers than aggressive sellers. I use this to see how aggressive either
> buyers or sellers are at the specific price."

*(15:31)*

> "Column number three is a volume profile that is colored by the delta. So if
> the delta is positive, you're going to see the color be blue, and if the
> delta is negative, you're going to see the color be red. But the
> distribution is done based on the total volume. […] The larger the profile,
> the more volume that we see."

> **Editor —** The 84 and the +216 are on the slide and in the card. The 366
> total volume is spoken over the chart and not verified, though it passes the
> parity check a real delta must (both even). The captions heard "26 more
> aggressive buyers"; the slide says 216. "Fair value" here is a per-bar
> notion, the busiest price inside a five-point bar, not the session value
> area the Vorwald channel builds its method around.

**The read** *(16:13)*

> "This is the basis to my trading strategy. I'm looking, and I'm feeling out,
> how aggressive the participants are. If there's a lot of aggressive
> participants entering the market at a certain price but no follow-through,
> it's a sign of a possible reversal in the market. If the market has a lot of
> strong selling volume but the market's not moving lower, so let's just say
> we're moving down, we're moving down, and right here we see a lot of selling
> volume, but as soon as we see the greatest selling volume of the day it's
> not moving down. Well, we're seeing a lot of aggressive participants. Maybe
> somebody's buying this move, and it's a good chance a buyer is active.
> Remember, aggressor hitting a passive participant. And it's a good chance
> the market may want to reverse. […] And maybe this is why the lower wick
> forms, and you only got that lower wick after it was placed. But by reading
> this volume you could get in in real time, saying, hey, if I'm correct on
> this thesis, maybe a lower wick will be placed here, because there's true
> buyers active in the market. […] If you're so aggressive and you're not
> making money, you become trapped if the market moves against you, and this
> is how we can look to capitalize on reversals."

> **Editor —** The Vorwald channel reaches the same mechanism from the other
> side (usho6UVLqkE, 14:24): a buyer repeatedly lifting a level, price failing
> to advance, a large seller absorbing. Neither cites the other. Note how he
> closes the loop on the wick: the footprint lets you buy the wick while it is
> forming, not after.

**No threshold** *(17:42)*

> "Looking at my delta footprint, again five-point range or 20-tick range, I'm
> looking for outliers in the data. A lot of people always ask me, hey
> Carmine, like, are you looking for a specific number? Are you looking for
> greater than 100, 500 […]? And I don't have an answer to that, because what
> I am looking for is unusual activity, or outliers in my data."

> **Editor —** The one place in eight episodes where the missing threshold is
> declined rather than merely absent. The corpus never gets one. The Vorwald
> channel's 250–300 contracts is the size of a resting ES order in the book, a
> different quantity, and that channel gives no delta number either.

**The trade** *(17:25)*

> "So this was a trade that I took. This was a $21,000 profit off of about
> $2,200 worth of risk. It was a nine-to-one risk-to-reward ratio, and I'm
> able to get great risk-reward ratios when I use the order flow to confirm
> the setups."

*(18:03)*

> "Down here we could see the greatest negative delta of the day, which was
> −735 and −1171, as the market was making a low. So as the market's selling
> off and moving lower, the greatest volume, or the most aggressive the
> sellers were all day, was at the low of day. So think about that. If a lot
> of selling is coming in at the low of the day, ideally, in an auction, you
> would see it continue moving lower. Now this is what the market looks like
> despite all of this selling. […] We cannot see this selling strictly looking
> off of this candlestick chart. Like, I don't see anything right here that
> indicates sellers are present in the market, or even buyers for this case.
> But reading the order flow, you could see that the selling was the most
> aggressive down here. −735 delta, −1171 delta. Eventually the market
> reversed, strong buying came in thereafter, and these sellers at the low
> became trapped. There were tons of effort but no reward by those sellers,
> and this is the only option for the market to do, is then move up."

*(19:24)*

> "Here's all that selling, right? Would you buy the market right here, at
> this moment, right down here? Would you buy the market? Honestly, this looks
> weak, right? We're making lower lows, we're also making lower highs. This
> looks weak. Nothing here tells me to buy the market. But everything right
> here tells me to buy the market. […] This is how I was able to catch the
> market long down here. Not up here, not up here. Down here, where all the
> selling volume came in."

> **Editor —** The journal on screen reads $21,750 on 30 contracts, 14.5
> points, $2,250 of risk, planned 8.33R, realised 9.67R; stop 5739.0, target
> 5753.0, which puts the entry at 5740.5. Every figure closes arithmetically
> and was checked against frames. He rounds all three when he speaks. The same
> trade returns in episodes 7 and 8, and episode 7's Bookmap tooltip shows the
> −1171 at 5739.75–5740, so the outlier is corroborated from a second
> instrument. What no episode shows is a loss.

**In real time** *(19:57)*

> "Down here at the low, we could see some selling volume step in. It's really
> not aggressive just yet. It's −367, −339. It's about average, or up to par
> with what we were seeing previously in the auction. But watch as I play
> this. The market's going to come into the low, and the selling volume is
> going to build. Right there, somebody hit the bid aggressively. Aggressive
> sellers just came in. […] Despite those aggressive sellers coming into the
> market, the market actually bounces. Right there, hit the bid aggressively,
> the delta got stronger, got more negative, so more aggressive selling came
> in, but we didn't even move lower. Despite all that selling, that's a red
> flag a little bit if you're looking to capitalize on a downside move. This
> to me is starting to warm up for an upside reversal, because we're seeing
> all the aggressive sellers not successful in bringing the market lower. […]
> We're seeing the negative delta, −254, then boom, right there, −1100. That
> just went from −200 to −1100. That means 900 more aggressive sellers just
> came into the market, and the market did not move down. This is a little
> concerning to be a seller, and this is a little bit of a green flag to start
> looking to buy the market, if we put those sellers in pain and if those
> sellers become trapped."

> **Editor —** The replay figures (−367, −339, −254, −1100, "900 more") come
> from the auto-captions, which garbled the last as "−11100"; his own next
> sentence fixes it. None is in the card and no frames were pulled for this
> window, so treat them as unverified. The shape is what matters: he is
> reading confirmation inside the bar, before it closes. That is the C of
> episode 7's CLC rule, where waiting for the close is what turns a two-point
> stop into a seven-point one. The Vorwald channel says the opposite, closes
> not wicks, four times over, and SMDX's change of character is a close below
> the last higher low. This is the cleanest split in the corpus and this
> replay is Carmine's side of it.

**The failed breakout** *(21:36)*

> "How many of you would say that this is a bullish move, breaking above a
> resistance level? We got a strong breakout above it with a strong green
> little rally candle, right? You see this really large rally candle here, and
> everybody's buying the breakout. You see volume here to confirm it, and
> you're thinking this thing is going to go to the moon. […] Well, reading the
> volume would tell you that this breakout is not very strong. […] As the
> market breaks out, the volume dissipates and the volume gets weaker."

*(22:17)*

> "In real time, when this was breaking out, let's act like you don't know
> what happens next. It looks strong with a candlestick chart. But reading the
> volume, you would see here that there's a lack of interest. There's almost
> like a volume tail, and I use this term again in episode number one. This
> volume tail shows that nobody cares about the market above this resistance
> level. If no buyers care about this move, then sellers are going to be
> forced to lower their prices. […] And again, this is just simply the volume,
> and not even looking so much at the delta. This volume tail right here tells
> me that the buying got shut down, the buyers became exhausted, and nobody
> cared about this move. Nobody cared about the market being up there."

*(23:13)*

> "The market just broke this resistance level, and watch when the volume
> builds and we leave a volume tail. So there's a lot of volume trying to come
> in here. We tried to move up, it immediately got shut down, and now things
> are starting to turn red, and indicate that no buyers want to buy this move,
> and sellers are now active, because things are turning red. And this is how
> you're able to capitalize on a downside sell-off move, shorting this failed
> breakout."

> **Editor —** The level on screen is labelled RESISTANCE HIGH (5733.5). This
> is the one setup in the episode the card leaves unverified; no frames were
> pulled, and the thin prints at the top are Gemini's reading alone. No stop
> or target is given for it. The mechanism is the mirror of the first setup,
> an absence of buyers where the first was an excess of sellers, and it is the
> same shape the Vorwald channel draws as a buying or selling tail in TPO
> letters (K8qtT2_axPo) and that SMDX names from the other side as "your
> breakout entry = their exit liquidity". Three schools, one trap.

**Closing** *(23:37)*

> "I'm telling you all, the greatest edge for short-term trading comes from
> understanding the responsibility, or the perception of price, from other
> participants. And the only way you can do this is reading the volume and the
> transactions coming in. A footprint chart is a good visual, but it's just
> one of the tools to be able to read the volume and the transactions coming
> into the market."

---

*Cut from this read: the channel and series intro, the subscribe and
social-media appeals at both ends, the side-by-side "these charts are
identical" demonstration, and the restatements of the aggressor definition.
Episode 3, which he trails at the close, covers the DOM and Bookmap.*
