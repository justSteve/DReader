# Read: Trading Like A Pro: The Wide Butterfly Spread Technique

> **A wide butterfly is n² one-step butterflies, stacked 1, 2, …, n, …, 2, 1 across its centre strikes, and you can sell them one at a time as the index walks across their centres.**

- **Channel:** tastylive, host Tom Preston · **Segment:** "Cherry Bomb: The Butterflies Inside Your Butterfly" · **Uploaded:** 2026-08-26 · **Duration:** 10:58
- **Card:** [CARD.md](CARD.md) · **Watch:** https://www.youtube.com/watch?v=ZVvVgcX84F0

## In brief

Tom Preston calls this "an old floor trader trick", and it is one: a way of
seeing a wide butterfly not as a single bet on one strike at expiry but as a
bundle of narrow butterflies, each with its own peak. Take a fly whose wings
span two strike-steps, say 25/35/45 on a 5-point grid, and it is exactly one
25/30/35 fly plus two 30/35/40 flies plus one 35/40/45 fly. Four in all: the
steps, squared. Widen the wings to three steps and there are nine, stacked
1, 2, 3, 2, 1 across the centre strikes.

The reason to know this is a trade. A one-step butterfly is worth most when the
index sits on its centre, so a wide fly on a zero-day SPX can be harvested piece
by piece as the index moves across each centre, instead of being held to the
close for the one middle strike. On the day he films it the at-the-money piece
is worth about a dollar and the off-centre pieces fifty-five to sixty-five
cents.

He asserts the arithmetic and demonstrates it on a slide. He never says why it
works. This read does, and the reason turns out to be simpler than the slide.

## The argument

### The claim on the slide

The slide is a five-row table. Down the left, the strikes 25 to 45. Then the
wide fly, then its three claimed components, and the video's whole case is that
the rows add up.

| Strike | 25/35/45 fly | 1 × 25/30/35 | 2 × 30/35/40 | 1 × 35/40/45 | Row sum |
|---|---|---|---|---|---|
| 25 | +1 | +1 | | | +1 |
| 30 | | −2 | +2 | | 0 |
| 35 | −2 | +1 | −4 | +1 | −2 |
| 40 | | | +2 | −2 | 0 |
| 45 | +1 | | | +1 | +1 |

They do. The 25 strike carries one long, the 30 nets to nothing, the 35 nets to
short two, the 40 nets to nothing, the 45 carries one long: the original fly,
reassembled from four one-step flies. His rule for the count is to take the
strike-steps in one wing and square them. Two steps, four flies. In the live
example the wings are 15 points on a 5-point grid, three steps, nine flies.

That is where the video stops explaining. What follows is ours.

### Why the weights are 1, 2, 1, and 1, 2, 3, 2, 1

Forget contracts for a moment and draw what a long butterfly pays at
expiration. It is a tent: nothing below the low wing, rising a point for every
point the index climbs past it, peaking at the centre, falling back to nothing
at the high wing. The tent's height is the width of one wing. A one-step fly on
a 5-point grid is a tent 5 points tall on a 10-point base. The 7660/7675/7690
fly is a tent 15 points tall on a 30-point base. Same shape, three times the
size in every direction.

Now try to build the big tent out of small ones. A small tent centred on 7670
stands 5 points tall at 7670 and is exactly zero at 7665, at 7675, and
everywhere beyond. That is the whole trick. At any strike on the grid the only
small tent with any height is the one centred on that strike; its neighbours
have already touched the ground. So to match the big tent's height at a given
strike you need precisely as many small tents centred there as it takes to
reach that height, and there is no other way to get it.

Read the big tent's height at each interior strike and divide by the 5 points a
small tent stands:

| Centre strike | 7665 | 7670 | 7675 | 7680 | 7685 |
|---|---|---|---|---|---|
| Height of the wide fly's tent | 5 | 10 | 15 | 10 | 5 |
| One-step flies centred here | 1 | 2 | 3 | 2 | 1 |

The triangle is not a curiosity of the arithmetic. It is the silhouette of the
wide fly, sampled at its strikes. For two-step wings the heights are 5, 10, 5,
hence 1, 2, 1. For wings of any width the counts climb by one per strike up to
the centre and fall by one per strike after it.

Two loose ends turn the picture into a proof. Between adjacent strikes every
option payoff is a straight line, so two positions that agree at every strike
agree at every price in between; matching the heights is enough. And the tents
are only the contracts drawn differently, so whatever reproduces the payoff
reproduces the position, which is the row-sum check on his slide. We also
solved the contract equations directly for both cases in the video: the
triangular weights are the only solution, not one decomposition among several.

### Why they sum to n²

Add the triangle: 1 + 2 + … + n + … + 2 + 1. The neatest way to see that this
is n² is to draw an n-by-n square of dots and count it along the diagonals. The
diagonals have lengths 1, 2, 3, up to n, and back down to 1. The triangle is a
square read cornerwise.

The tent gives the same answer with more meaning. In strike-steps, the big tent
has base 2n and height n, so its area is n². A small tent has base 2 and height
1: area 1. Areas add, so the big tent holds n² small ones. "Square the strike
steps" is not a mnemonic. It is the area under the payoff.

### It is an identity in prices, not only at expiry

Here is the part the video shows without saying, and it is the part that makes
the trade make sense. The decomposition is a statement about contracts, not
about expiration, so it holds at every moment of the day: the price of the wide
fly is always the price of its nine embedded flies, each counted with its
multiplicity. We checked this against the option chain visible on his screen
just before he starts pricing pieces. At the mid, the one-step flies centred on
7665, 7670, 7675, 7680 and 7685 were worth 0.825, 0.95, 0.80, 0.55 and 0.30.
Weight them 1, 2, 3, 2, 1 and the total is 6.525, which is the wide fly's own
mid on the same chain and the "$6.50" he reads aloud. Repeating the check on
the chain a minute later, with the wide fly at 6.75, balances again.

So when he says the at-the-money piece is worth 95 cents and the piece two
strikes away 55 cents, he is not comparing unrelated instruments. He is pointing
at the parts of one thing and saying which parts are currently expensive. With
SPX at 7668 the two flies centred on 7670 are the richest, and they sit inside a
position whose whole is, to the cent, the sum of them.

### The trade

Which makes the method almost obvious. A one-step fly is dearest when the index
sits on its centre. As a zero-day SPX drifts across the strikes, first one
embedded fly and then another comes to its peak, and each can be sold out of
the wide fly as it does, rather than waiting for the close and hoping the index
pins the one middle strike. The piece comes out at its own price as a one-step
fly. What remains is the other pieces, which are still long butterflies, so
still a defined-risk position that can only pay out or expire. He says it his
own way: "I'm just left with some other butterflies."

How much room is there? Holding the wide fly to the close pays at most 15
points, and only if the index settles on 7675. The nine pieces each top out at
5 points, so the theoretical ceiling for harvesting them one at a time is 45
points, three times the hold-to-expiry maximum, which is simply n² pieces of
height one against one piece of height n. Nobody collects that: it would need
the index to visit every centre at the moment of expiry. What he actually shows
is a piece worth about a dollar when the index is on its centre against
fifty-five to sixty-five cents when it is not, sold with hours still on the
clock. That gap is the edge, and it is paid only to someone watching the chain
and fast enough to act. He is candid about this: the technique needs speed, a
written record of which flies are on, and practice. He also says he rarely puts
on a wide butterfly as such; he arrives at one by covering the short vertical
inside an unbalanced fly, and then harvests if the index starts oscillating.

One more thing the demonstration teaches, though not on purpose. The order
panel on his screen reads Limit 7.60, Max Profit 740, Max Loss −760: the
ticket's profit and loss are computed from a limit price that had gone stale,
and 15 − 7.60 = 7.40 confirms it. What he says aloud is $6.50, which is the
live mid on the bid/mid/ask strip beneath the ticket. An earlier automated pass
over this video reported the ticket as Limit 6.50, Max Profit 850, Max Loss
650. Those numbers do perfect arithmetic, 15 − 6.50 = 8.50, and they are not on
the screen. They were computed from the spoken price and reported as if they
had been read; pulling the frames settled it. A set of figures that satisfies
its own equations has proved that it coheres, not where it came from.

### Where it sits in the corpus

Almost nowhere, and that is worth saying plainly. Nearly every card in this
corpus is about reading order flow to time an entry: Carmine Rosato, the SMDX
series, Vorwald, Trading Notes. The one other card that touches options at
all is fvid's "Asymmetric Value", an AI-generated piece about selling
cash-secured puts on beaten-down single names over months, and it shares
nothing with this one but the instrument: different underlying, different
horizon by three orders of magnitude, and no view on structure or pricing.
Preston's lesson is about the anatomy of a position rather than the tape.
There is nothing here for him to agree or conflict with, and we have not
manufactured a link. If the corpus grows an options-structure axis, this is
its first entry.

## In his words

**What a butterfly is for** *(00:00)*

> "Butterfly trades. Buy one, sell two, buy one. You get it. And butterflies are
> one way to trade, you know, trying to pinpoint where a stock will be at
> expiration. So a butterfly, for example, will maximize its value when the
> stock or index is at the center strike, at the short strike, at expiration."

**An old floor trader trick** *(00:26)*

> "But here's an old floor trader trick for evaluating butterflies. And it's not
> necessarily an advanced topic, and it's not something that you're going to
> trade all the time with, but it's something that if you're trading
> butterflies, I think you should be at least aware of."

**The slide** *(00:49)*

> "So what I have loaded up here is an example. I just picked some strikes, 25,
> 30, 35, 40, 45, just to make it clear and simple. What I'm showing you in the
> far left-hand column here is a 25… calls or puts, it does not matter. Calls
> or puts, it doesn't matter, okay? So, buying one of the 25, let's call them
> puts, 25 puts, selling two of the 35 puts, and buying one of the 45 puts.
> Now, what's all this gobbledygook to the right side? I'm going to show you
> that that 25/35/45 put butterfly is comprised of four other butterflies.
> What? Okay, follow along as I go through this."

> **Editor —** "Calls or puts, it doesn't matter" deserves its own line. A call
> butterfly and a put butterfly on the same three strikes have the same payoff
> at expiry, so everything that follows is about strikes and quantities, not
> about which side of the chain they came from.

**The three components** *(01:45)*

> "On the left-hand side I have the 25/35/45 put butterfly. Next to it, I
> loaded up the 25/30/35 put butterfly. So it's buying one of the 25s, selling
> two of the 30s, buying one of the 35s. Next, I go and buy two of the 30/35/40
> butterflies. That's buying two of the 30s, selling four of the 35s, and
> buying two of the 40s. Finally, I go and I buy one of the 35/40/45
> butterflies, buying one of the 35s, selling two of the 40s, buying one of the
> 45s."

**Adding across the rows** *(02:35)*

> "What does all this mean? So, on those three butterflies on the right-hand
> side, add them up across the rows. So what do I have when I buy the 25/30/35
> put butterfly? I buy one of the 25s. That matches up with the original long
> one put at the 25 strike. Now, go down to the [30] strike. What do I have? A
> minus two and a plus two. Those cancel each other out. So I have zero at that
> strike. Now I go to the center row, the 35 strike. Of those component
> butterflies, I have long one of those puts, short four of those puts, and
> then another long one of those puts, for a net short two. That matches up
> with a short two 35 puts of the original butterfly. Now I go to the 40
> strike. I'm buying two, selling two of the component butterflies at the 40
> strike. They cancel each other out. Finally, that last butterfly that I'm
> buying gives me long one of the 45 puts."

> **Editor —** He says "35" for the second row. The slide's second row is the 30
> strike, where −2 and +2 cancel, and he implicitly corrects himself a sentence
> later by calling 35 "the center row". Bracketed above.

**The rule** *(03:47)*

> "What does this mean? Whenever I have a butterfly where there's more than one
> strike increment between the longs and the shorts… one strike increment
> would be 25 to 30, 30 to 35. That's one step for the strike prices. Whenever
> I have more than one step in my butterfly strikes, I have multiple
> butterflies embedded in it. In other words, I have multiple one-step
> butterflies embedded in it. How many do I have? Enough time for a little bit
> of math. I take how many steps between my strikes: in this case, 25 to 30 is
> one step, 30 to 35 is two steps. Take the steps, square it. Two times two is
> four. That's how many butterflies are embedded in that 25/35/45 butterfly.
> So one 25/35/45 butterfly contains one 25/30/35 butterfly, two 30/35/40
> butterflies and one 35/40/45 butterfly."

> **Editor —** This is the assertion the video never explains. The one, two,
> one are the heights of the wide fly's payoff tent at 30, 35 and 40, measured
> in one-step tents, and the square is the tent's area. See "The argument"
> above.

**Why you would want to know** *(05:13)*

> "Why would I ever need to know this? When you are trading butterflies,
> particularly with zero DTE or very short-term options, what you can sometimes
> do is capture the maximized value of these embedded butterflies."

**The SPX example** *(05:36)*

> "Let's go take a look at the SPX options right now. What I have loaded up
> here is a 7660/[7675]/7690 put butterfly, and it is for a $6.50 debit. Now,
> what I just told you is, when I have how many steps between the strikes? 60
> to 65 is one. 65 to 70 is two. 70 to 75 is three. What do I do with that? I
> square it. Three times three is nine. I have nine butterflies in here."

> **Editor —** The caption drops the middle strike; the order panel supplies
> it: buy 1 of the 7660 put, sell 2 of the 7675, buy 1 of the 7690, SPX
> zero-day, 25 August 2026, with the index at 7668–7669. The "$6.50" is the
> live mid on the strip beneath the ticket (bid 6.25, mid 6.50, ask 6.80). The
> ticket itself still reads Limit 7.60, Max Profit 740, Max Loss −760,
> computed from a limit that had not been refreshed; 15 − 7.60 = 7.40. An
> earlier automated pass reported the ticket as 6.50 / 850 / 650. Those were
> worked out from the spoken price, not read from the screen; the frame at
> `frames-552-600/f_0008.jpg` settled it.

**The trading card** *(06:17)*

> "So what I'll do, and this is something, again, you should trade this style
> on the floor, and it's handy to be able to have a trading card. You used to
> write this stuff down by hand. Now you can use a spreadsheet to keep track of
> it, but once you do it a few times, you'll figure it out. What I have is one
> of the 7660/65/70s, two of the 65/70/75s, three of the 70/75/80s, two of
> these and one of these. So as the index moves up and down around these
> strikes, the embedded butterflies are going to have maximum values wherever
> the index is."

> **Editor —** "Two of these and one of these" are the 7675/80/85 and
> 7680/85/90 flies. One, two, three, two, one: nine.

**Which piece is worth what** *(07:03)*

> "So for example, let's look at this one. With the index at 7669, the
> [7665/7670/]7675 put butterfly is worth 95 cents. Let me move this up to this
> butterfly. This 75/80/85 is only worth 55 cents. If I go down here… if I buy
> this one, sell two of these, and buy one of these, this butterfly is only
> worth 65 cents. Remember, this one, for the out of the money, is worth a
> dollar."

> **Editor —** The three prices are parts of one thing. From the chain on
> screen at 05:59, the flies centred on 7665, 7670, 7675, 7680 and 7685 were
> worth 0.825, 0.95, 0.80, 0.55 and 0.30 at the mid; weighted one, two, three,
> two, one they sum to 6.525, the wide fly's mid on the same chain. That is our
> arithmetic from `frames-552-600/f_0008.jpg`; of the per-fly figures only the
> 0.95 and the 0.55 are in the card. Two cautions on his words. The caption
> has "out of the money" for the dollar fly; the fly he is pointing back at is
> the at-the-money one he has just priced at 95 cents. And the 65-cent fly is
> hard to place: he heads for "the 60 strike or the 50 strike", drags the
> wrong legs, and no frame covers the moment. The card names it
> 7645/7650/7655, which is an inference. On the 05:59 chain a fly centred that
> far below the index was worth about 30 cents, so 65 cents fits a fly one or
> two strikes below the money better. Treat the 65 cents as unverified and its
> strikes as unknown.

**The harvest** *(08:08)*

> "So, with the index moving around from 7668, close to 7670: if it drops down
> to 7665, then maybe I'll sell these two put butterflies that I have embedded
> here. If it rallies up to 7675, that'll maximize the 70/75/80 butterfly."

> **Editor —** Note the "maybe": this is an option he keeps, not a rule. Note
> also "these two". By his own count there is one fly centred on 7665, the
> 7660/65/70, and three centred on 7675, so whichever pair he is pointing at,
> the principle is what to keep: when the index sits on a centre, the piece
> centred there is the dear one, and that is the piece to sell. The card
> records this moment as selling "the two 7660/7665/7670 flies"; the strikes
> are not in his words.

**What it takes** *(08:30)*

> "So this is an advanced way of looking at butterflies. Are you going to use
> this trading strategy? You're going to be very fast. You have to be very
> fast, and know which butterflies you have on. Takes a little practice, but
> like I said, a spreadsheet can really help you. But it is a way to maximize
> the value of your butterfly trading."

> **Editor —** What he does not say: a one-step SPX fly is a four-leg order,
> and on a piece quoted near a dollar the bid-ask and the fees on four legs are
> not a rounding error. The dollar-against-sixty-cents edge he shows is before
> those costs.

**Where the wide butterflies come from** *(08:57)*

> "I don't trade a lot of butterflies straight up as themselves. I'll do
> unbalanced butterflies, embedded short vertical, things like that. But a lot
> of times after I have one of those unbalanced butterflies on, and I cover the
> embedded short vertical, I'm left with a butterfly. And I'll use this
> technique if the index is moving around a lot from one strike to another
> strike and back, and up and down and up and down. I'll use it to try and
> maximize my profits. And again, when I close out the embedded butterflies
> that are inside the wide butterfly, I'm just left with some other
> butterflies. They're defined-risk trades."

> **Editor —** He is right that what remains is defined risk, and the reason is
> worth having. Every embedded fly is long, and you only ever sell pieces you
> hold, so the count at each centre never goes below zero. A non-negative
> stack of long butterflies pays zero or better at every price, and its worst
> case is whatever net debit is still outstanding. Sell the two 7670-centred
> pieces out of a 1, 2, 3, 2, 1 stack and you hold 1, 0, 3, 2, 1: an odd-shaped
> tent, still a tent.

**Homework** *(09:46)*

> "So what I would do is review that little slide that I showed you. Look at
> some of these butterflies in the S&P's. Look at their prices. See how their
> prices change throughout the day. You can have these loaded up. You don't
> even have to route them as orders. Have them loaded up and look at how their
> prices change as the index prices change. That's going to let you manage
> these with even greater sophistication and confidence."
