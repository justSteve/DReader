# Scenario episode set — practice material for `narrating-orderflow` [dr-22w.4]

Nine episodes from Strader's ES tape, two for each row of the skill's scenario
table and one that fits no row. Each is a moment in a real session with a hard
cutoff: everything the narrator may see is in `facts.json`, everything that
happened afterwards is in `aftermath.json`, and the scenario, the detector
readout and the verdict are in `key.md`.

Built by DReader against `market.orderflow` **read-only** — nothing in this set
writes to Strader's repo. Steve's calls, 2026-09-18: nine episodes; the selector
lives here.

## The set

| id | row | day | cutoff CT | the level | what it is | what happened next |
|----|-----|-----|-----------|-----------|------------|--------------------|
| ep01 | A · selling into a level | 2026-08-26 | 09:28 | 7680.50 (session low 7678.75) | two biggest sell minutes of the day, a quarter point of reward | held, +13 |
| ep02 | A · selling into a level | 2026-08-31 | 13:27 | 7690.75 (overnight low 7691.50) | biggest sell minute of the day at a level defended since 08:33 | **gave way at 13:32, −14** |
| ep03 | B · buying into a level | 2026-08-26 | 10:11 | 7697.00 (overnight high 7698.25) | buyers pressing on 0.7× volume, a point short of the obvious price | held, −12.75 |
| ep04 | B · buying into a level | 2026-08-03 | 13:54 | 7634.25 (session high 7635) | +1,157 into the high of a 92-point day, given straight back | **gave way at 14:01, +5.25** |
| ep05 | C · at a spot obvious traders just acted | 2026-08-17 | 09:41 | 7790.50, the session low, 3 minutes old | three stacked sell minutes, half a point, then a bid | held, +6.75 |
| ep06 | C · at a spot obvious traders just acted | 2026-08-14 | 10:00 | 7809.50, the session low, 1 minute old | −835 break, instant 3-point bounce on +28 delta | **gave way at 10:08, −12.5** |
| ep07 | D · acceptance after an aggressive move | 2026-08-28 | 11:13 | 7745.25, the accepted area's ceiling | −20 leg, 10 quiet minutes on two-thirds the volume | continued, −20 |
| ep08 | D · acceptance after an aggressive move | 2026-08-07 | 14:26 | 7775.50, the accepted area's floor | +14.75 leg, 8 quiet minutes under the overnight high | **neither: ±0.25 at 45 min** |
| ep09 | null — no row fits | 2026-08-12 | 13:10 | none within 9.25 points | 0.3–0.7× minutes, ±2 points, nothing near | quiet drift, +6.25 |

Four of the eight scenario episodes go the read's way and four do not, which is
deliberate: a set where absorption always resolves teaches prediction, and the
skill forbids prediction. ep05 and ep06 are the same shape three minutes apart
in session time with opposite outcomes, and the evidence that separates them is
present at both cutoffs.

Coverage: four mornings, two middays, three afternoons; days from 19 to 92
points of range and from 0.6× to 1.5× pace; one day (2026-08-26) appears twice,
at opposite ends of its range 43 minutes apart.

## Using an episode

1. Hand a fresh agent the skill and `epNN/facts.json`, with the prompt at the
   bottom of `epNN/briefing.md` (it is the same prompt for every episode, and
   the same one both 2026-08-24 narrations answered).
2. Grade the narration against the six moves and the self-check in SKILL.md.
3. Only then open `epNN/key.md`, and `epNN/aftermath.json` for the path.

`briefing.md` is the same fact sheet rendered for a human — use it to try the
episode yourself, or to check a claim a narration made.

## How the episodes were chosen

`scan.py` sweeps corpus days and scores candidates for each row; every finalist
was then read against the tape by hand, and its level, its scenario and its
outcome were verified before it entered the set. The scanner's thresholds are
prompts to look, never verdicts — the skill's own rule about detector events.

Selection is allowed hindsight (it may look at the whole day to pick a moment).
The fact sheet is not: every field in `facts.json` is causal to the cutoff.

Two calibration corrections are baked into the scanner and are worth knowing:

- **Absorption is found by delta share, not by volume.** The known case
  (2026-08-24 10:41–42) is 1,796 and 2,627 contracts against a 2,484 median
  minute — 0.9× and 1.1×, not a surge. What makes it absorption is one-sided
  aggression at a level (−615 over two minutes, 56% of the day's largest sell
  minute) with zero displacement. A volume threshold cannot find it.
- **Acceptance is read off raw minutes, not off `moves.segment_moves`.** A
  zigzag leg ends at its extreme *because* price later retraced the reversal
  threshold, so sampling the minutes after a leg end selects the start of the
  counter-move by construction. The first cut did that and produced seven
  acceptance candidates in two months, none of which continued.

## What the detectors said — the second half of this set's job

Each episode carries `detectors.txt`: `tape_events.TapeEventDetector` and the
developing effort/effect cells replayed causally to the cutoff, run twice, from
the RTH open and from the prior 17:00 Globex open.

**1. No `ABSORPTION-CLUSTER` fired at any of the six absorption episodes.** The
only cluster anywhere in the set is ep01's, twenty minutes before its episode
and only in the Globex framing. The class wants effort ≥ 80 and effect ≤ 10 for
two consecutive bars; real absorption at a level routinely shows ordinary volume
with heavy one-sided delta and a small but non-zero displacement, and never
satisfies it.

**2. The superlative is the mechanical antecedent that does fire.** A
`SUPERLATIVE MAX-SELL-DELTA` landed in the cutoff minute or the one before it in
ep01 (09:25, 09:27), ep02 (13:26) and ep06 (09:59); ep05 had one six minutes
earlier. ep03 and ep04 — both "the effort is unremarkable, the level is what
matters" cases — produced nothing at all. If a live narrator is to be woken for
Carmine's absorption scenario, the superlative class plus a level test is the
wake condition; the absorption class as tuned is watching for a different shape.

**3. Acceptance has no event class.** ep07 and ep08 emit nothing in either
framing. Acceptance is defined by what stops happening, and every class in
`tape_events` watches for something starting.

**4. The absorption class's own calibration numbers come from the overnight
sample.** `tape_events` documents its threshold against 2026-08-24 10:41–42 at
effort 84.7 and 90.4. Measured 2026-09-18: those figures reproduce **only** when
the atom stream starts at the previous 17:00 Globex open (84.7 / 90.4); from the
capture start at 02:50 they are 79.1 / 87.0, and against the RTH session alone —
the session the narration is about — the same two bars rank **26.1 and 54.5**,
i.e. at or below the median minute. The effect ranks (6.3 / 6.4) are robust; the
effort ranks are not. Across this set the same inversion is everywhere: ep03's
stall is F4 (effort 2.6–27.6) from the RTH open and F1/F2 (86–88) from the
Globex open; ep09's dead air is F4 against RTH and F2 — absorption — against
Globex. It is the same finding as st-dioq ("the F 2×2 is largely a session
detector"), landing on the threshold that was set from printed floats. This is
Strader's to rule on; DReader only measured it.

## Tape quality found while building this

- **The ES capture rolled late.** The corpus holds ESU6 through 2026-09-17 and
  switches to ESZ6 on 2026-09-18, while volume had already left: 2026-09-14
  prints 522k contracts, 09-15 169k, 09-16 111k (on a 122.75-point range),
  09-17 56k, against a ~1.0M median. Any measurement over 2026-09-14 → 09-17 is
  of a dying book. `scan.py` now refuses a day under half the recent median
  volume, which also excludes holidays (2026-09-07).
- **A corpus day is a calendar day in CT**, so the evening session that opens at
  17:00 sits in the *previous* day's file. The overnight range must span two
  files. It did not in the first fixture: `test/briefing-1043.md` reports
  "Overnight (Sun 17:00 → 08:30): high 7686.5" for 2026-08-24, but the true
  window high is **7703.25** — the figure quoted is the midnight-to-open range.
- Walking further back than one calendar day to find an evening session splices
  a stale one in: 2026-08-31 is a Monday whose Sunday reopen is missing from the
  corpus, and a multi-day search labelled the *previous Thursday* evening as its
  overnight. Each fact sheet now states the window it actually measured.
- 2026-08-03 has no prints before its open at all; its fact sheet carries no
  overnight range rather than a fabricated one.

## Rebuilding

Run with Strader's interpreter (it has the corpus dependencies); day files are
cached under `.cache/` (gitignored, ~1 s per day after the first read).

```bash
S=/root/projects/Strader/.venv/bin/python
$S scan.py --start 2026-08-03 --end 2026-09-17 --top 10        # candidates by class
$S factsheet.py --id ep01 --day 2026-08-26 --cutoff 09:28 --level 7680.5 --defends low
$S render.py ep01 > ep01/briefing.md
$S detectors.py --day 2026-08-26 --cutoff 09:28 > ep01/detectors.txt
```

`tape.py` is the read-only door onto the corpus; everything else goes through
it. The exact arguments that built each episode are in its `facts.json` header
and in the table above.
