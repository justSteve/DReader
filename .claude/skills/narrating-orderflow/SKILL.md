---
name: narrating-orderflow
description: Use when describing live or replayed futures tape (footprint, delta, volume-at-price, DOM) to a trader in prose — narrating an absorption, trapped-participant, acceptance or heavy-selling scenario as it develops, or reviewing why a narration read as a recitation of numbers rather than a read of the market
---

# Narrating Orderflow

## Overview

A tape narration is a **read**, not a readout. The trader can see the numbers;
what they cannot see is what the numbers add up to. Carmine Rosato's course
narration (`media-reader/dossiers/it-orderflow-*/transcript.txt`) states the read
in plain words first and uses a number only as the tell that earns it:
*"buyers are showing a ton of effort at high of day and they are not getting
rewarded"* (trapped-4304 4:56). Reference moves with timestamps:
`carmine-moves.md` in this directory.

**Core principle:** every adjective carries its tell, every number carries its
scale, and the trader leaves knowing who is on the wrong side and what to
watch next.

## The six moves (say them in this order, each in a sentence or two)

| Move | Question it answers | Carmine's form |
|---|---|---|
| Context | Why does this spot matter today? | level + what happened here earlier |
| Effort | Who is aggressive, how big *for this day*? | "tons of buying" then the print |
| Result | What did price do versus what that effort should have done? | "40 minutes, less than a 5-handle range, despite all this buying" |
| Inference | Who is on the wrong side and what do they need? | "if I'm a buyer here I'm not excited to be long" |
| Expectation | The one observable you want to see next | "you wanna see these rallies fail" |
| Invalidation | What proves the read wrong, and what you do then | "if that level fails and acts as resistance, I'm exiting" |

Lead with the read in one sentence before any of the six. End on
expectation + invalidation. 120–220 words per utterance.

## Scale: numbers are evidence, never the sentence

A size is only a size against a named comparison set. Choose the set to fit
the question, and say which one you used:

- **The day so far, qualified by the day's character.** "Heaviest minute
  since the open" on a day that has already moved thirty points is a different
  sentence from the same words on a day that has moved eight. State the
  character in the context move so every later size word inherits it (Carmine:
  "depending on the conditions, depending on the average range" — 0916-1339 2:02;
  "the rally was done on lower volume by time" — trapped-4304 2:19).
- **Local references over whole-session ranks.** Minutes stuck in how many
  points; what the same effort bought an hour ago; how much of this price's
  volume arrived just now; the heaviest hit *this level* has taken today.
  These survive the time of day. A whole-session percentile does not: by the
  afternoon it ranks every minute against the opening hour.
- **Cross-day references name their day type.** "A normal 14:00 minute" means
  nothing unless it is a normal 14:00 minute *on a day like this one*. Never
  compare to calendar-adjacent days; compare to same-type days, or not at all.
- **Detector events and percentiles are prompts to look, never verdicts to
  narrate.** They tell you where to point your attention; the read still has
  to earn its sentence from effort, result and context. Percentiles do not
  belong in the fact sheet the narrator reads from.


- Say the size in words **relative to the session**, then the print if it helps:
  *"the busiest minute of the morning, five times a normal one"* (12,921 vs a
  2,500 median), not *"12,921 contracts, 99th percentile"*.
- One number per sentence at most. **Never a percentile in prose.**
- Convert every quantity: contracts → multiples of a normal minute or of the
  day's biggest; delta → against the day's biggest on that side; range → points
  and against what the same effort produced earlier; stall → minutes stuck in
  how many points.
- Delta only matters at a level that matters or as an outlier: *"if I see 5,000
  when the average is 600, I watch that price; a 993 in the middle of nowhere is
  nothing"* (absorption 23:31–24:42).

## Editorial license and its bounds

Every read says how much weight it can bear, in the trader's register, not in
numbers (Strader's "grades, not gates": a label near the line must say so).
"A fight at the level, not a resolved one" is a coin-flip spoken properly;
"they are trapped and they know it" is a strong grade and needs a strong tell.

You may say *absorbed, trapped, not getting paid, failing, giving up, stepping
in, defending, leaning on*. Each one needs its tell in the same sentence or the
one before: effort **and** the result that contradicts it. Without both it is a
guess, and the trader cannot check it.

You may not: attribute intent as fact ("a fund is covering"); predict ("this
will sell off"); state a rule as a law of the market ("low-effort advance means
a missing seller"); narrate anything the tape has not shown yet. Carmine's
frame is opportunity and risk, never prediction: *"do we know a setup is gonna
work out before we enter it? Absolutely not"* (absorption 25:33).

## Deriving inference, expectation and invalidation

The first three moves are read off the tape. The last three are looked up
from the pattern the first three make, then graded. Carmine's four scenarios
(Terms deck, `it-orderflow-terms-concepts` 12:09–35:39) each carry a fixed
triple; the judgment left after the lookup is (a) which side showed effort
without reward, (b) whether the level is one where obvious traders act, and
(c) how strong a word the tell earns.

| Pattern (context + effort + result) | Inference: who is wrong-sided | Expectation: the one observable | Invalidation |
|---|---|---|---|
| Selling into a low or level; price will not go lower (deck 12:09, 21:44; absorption chapter 0916-1108) | Sellers not paid; a passive buyer absorbing, shown or hidden | Dips into the level hold, then at-offer buying and a fast tape away | Level breaks and the bounce back into it is sold; it now acts as resistance |
| Buying into a high or level; price will not go higher (deck 16:10; trapped-4304, 0916-1339) | Buyers not paid; a passive seller absorbing | Rallies into the level fail, then at-bid selling | Level breaks and the dip back into it is bought; it now acts as support |
| Either of the above **at a spot where obvious traders act** — high/low of day, a breakout level, a stop cluster (deck 23:56) | Add *who*: breakout longs or shorts, and the stop-outs, are trapped | Pressure on them: price moves against them and their bounce fails | They get rewarded: follow-through in their direction |
| Aggressive move, then consolidation near the extreme on lower volume by time (deck 27:37, 31:58; 0917-0657) | Both sides accepting the new price; whoever fades the dips is the trapped one | Dips bought, higher lows (or the mirror), then continuation | The consolidation breaks against the move and the dip is not bought |

A read that does not fit a row is narrated as what it is — effort, result,
and "no clear scenario yet" — never forced into one (Carmine, 0917-0723 2:17:
"there's no real strong or clear absorption or any trapped participants").

## Cadence

Speak at decision points — a level test, a burst of effort, a stall, a failed
bounce — not per bar. Between them, silence. Every utterance stands alone:
someone who missed the last one must still get the read.

## Common mistakes

| Mistake | Fix |
|---|---|
| Ladder recited ("1062 sold vs 326 bought, −736") before the read | Say what it shows, then cite one figure |
| "Effort 85, effect 6" | "Sellers hit it as hard as anything this hour and it did not move" |
| Percentiles, cumulative delta, cell names in prose | Those are your inputs, not the trader's language |
| Adjective without tell ("clear absorption") | Name the effort and the failed result |
| Six numbers in one breath | One per sentence; drop the ones that do not change the read |
| Ending on a list of levels | End on one thing to watch and one thing that proves you wrong |

## Input contract (what the fact sheet must carry)

The narrator reads from a fact sheet, never from the raw tape or from a
detector's verdict. It must hold: the session's levels (open, high and low
with times, prior close and range, overnight range, where the big moves of
the day started); the day's character so far (range covered, pace); each
minute's effort as a multiple of the day's typical minute *and* the running
maxima on each side, buy and sell separately; result as displacement over
time at the level; volume at price at the level split by aggressor, with how
much of it is recent; and whether the level is one where obvious traders act.
No percentiles, no cell names. Everything observable at the cutoff, nothing
after it.

Every figure states the window it was measured over, and the sheet is built by
code that is tested, because the narrator cannot audit it: the first fixture's
"overnight range" was a midnight-to-open range labelled 17:00, and both graded
narrations repeated it (`episodes/README.md`, 2026-09-18).

**Practice episodes:** `episodes/` — nine cutoffs from the ES tape, two per row
above and one that fits no row, each with the fact sheet, the held-back
aftermath and a key. Four of the eight scenario episodes go the read's way and
four do not. `test/` is the RED/GREEN record for the skill itself.

## Self-check before you send

Count the numbers. More than one per sentence, or any percentile: rewrite.
Find each strong word and its tell in the same breath. Confirm the last two
sentences are expectation and invalidation.
