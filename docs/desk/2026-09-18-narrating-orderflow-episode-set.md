# Nine practice episodes for the orderflow narrator — what was built and what it found

2026-09-18 · bead **dr-22w.4** (closed) · commit `330fd70` · DReader

## In one paragraph

Last session left the narration skill with a single practice case, the
2026-08-24 absorption at 10:43. You asked for a set covering the whole range of
opportunities Carmine teaches. There are now nine: two for each of the four
scenarios in the skill's table, plus one where nothing is happening and the
narrator has to say so. Each one is a real moment in a real session with a hard
cutoff, built from Strader's own tape. Four of the eight scenario episodes go
the reader's way and four do not, which is the point — a practice set where
absorption always works teaches guessing.

## The nine

| | scenario | day, time | the level | what happened after |
|---|---|---|---|---|
| ep01 | selling into a level, price will not go lower | 08-26, 09:28 | 7680.50 | held, price rose 13 points |
| ep02 | same | 08-31, 13:27 | 7690.75 | **broke five minutes later, fell 14** |
| ep03 | buying into a level, price will not go higher | 08-26, 10:11 | 7697.00 | held, price fell 12.75 |
| ep04 | same | 08-03, 13:54 | 7634.25 | **broke seven minutes later, rose 5.25** |
| ep05 | the same fight where obvious traders just acted | 08-17, 09:41 | 7790.50, a low three minutes old | held, price rose 6.75 |
| ep06 | same | 08-14, 10:00 | 7809.50, a low one minute old | **broke eight minutes later, fell 12.5** |
| ep07 | a hard move, then quiet acceptance of the new price | 08-28, 11:13 | 7745.25 | continued, fell 20 more |
| ep08 | same | 08-07, 14:26 | 7775.50 | **neither — a quarter point away at 45 minutes** |
| ep09 | nothing is happening | 08-12, 13:10 | none within 9 points | a quiet drift up of 6.25 |

Four mornings, two middays, three afternoons. Days from 19 to 92 points of
range, and from two-thirds to one-and-a-half times normal pace. ep05 and ep06
are deliberately the same shape with opposite outcomes, and the evidence that
tells them apart is present at both cutoffs: the bounce in ep05 came after three
failed pushes and carried real buying, the bounce in ep06 carried almost none.

## What the machine saw, which is the other half of the job

Every episode also records what Strader's own detectors emitted at that minute.
Three results, and they are not what the code assumes.

**The absorption detector fired at none of the six absorption episodes.** Its
rule wants very heavy volume and almost no price movement for two minutes
running. Real absorption at a level routinely shows ordinary volume with heavy
one-sided pressure and a small but real movement, and never satisfies it.

**What does fire is the record-setting minute.** A new biggest-sell-minute of
the session landed on the cutoff minute or the one before it in three of the
six, and six minutes earlier in a fourth. The two episodes that produced nothing
at all are the two where the effort is unremarkable and the level is the whole
story.

**The detector's own calibration figures come from the overnight hours.** The
code documents its threshold against the 2026-08-24 case at effort ranks of 84.7
and 90.4. Those numbers reproduce only when the measurement starts at the
previous evening's five o'clock open. Measured against the trading session
itself — the session the narration is about — the same two minutes rank 26.1 and
54.5, at or below the middle of the day. The effect ranks hold up; the effort
ranks do not.

Both findings went to Strader as bead **st-d6k8**, along with a fourth: the
tape capture stayed on the expiring September contract through 09-17 while the
volume had already moved to December. On 09-16 the file holds 111,000 contracts
against a million-contract norm, on a 122-point range. Anything measured over
09-14 to 09-17 is measuring a dying market. It recurs at the December roll.

## A correction to the earlier fixture

The 2026-08-24 practice sheet says the overnight high was 7686.5. It was
7703.25. A corpus day is a calendar day, so the evening session that opens at
five o'clock sits in the previous day's file; the old builder read only from
midnight and called that the overnight. Both graded narrations quoted the wrong
figure — one as a target, one as "nine and a half points up" when it was 26.

Neither narrator could have known. The error entered through the fact sheet and
passed untouched through the narration and the grading, which is the argument
for the fact sheet being built by tested code and for every range stating the
window it was measured over. The new builder does both. The original file is
left as issued, because it is the record of what those two were given.

## What is open

- **The skill re-test you put on hold now has material.** Recommend ep02 (an
  afternoon where the read fails) and ep09 (the one with nothing in it) — those
  two punish a narrator for manufacturing a read.
- **Strader has st-d6k8.** The contract roll is the operationally urgent half.
- **A proposal arrived today on the same skill**: the Desk page
  `desk-2026-09-18-icm-applied-to-narrating-orderflow` (bead st-whl4) proposes a
  grading lane in DReader over these nine episodes. It has not been acted on.

## Where it lives

`DReader/.claude/skills/narrating-orderflow/episodes/` — nine folders, each with
the fact sheet, the held-back aftermath, a readable briefing, the detector
readout and an answer key, plus five tools that rebuild any of it. The ops
manual is the desk page `desk-narrating-orderflow-episodes-ops`.
