# Test fixture — 2026-08-24 10:41–42 CT absorption (Strader's calibration case)

RED/GREEN record for the skill, per `writing-skills`.

- `episode_factsheet.py` — builds the fact sheet from Strader's ES tape
  (`market.orderflow.tradesource`, `moves`); run with Strader's venv. Cutoff
  10:43 CT: `episode-facts.json` is what the narrator may see,
  `episode-aftermath.json` is held back (price ran to 7686 by 11:15; the
  sellers were absorbed).
- `narration-baseline.md` — fresh agent, same prompt, **no skill**: ~30 numbers
  in 350 words, raw percentiles, ladder recited before it is read, a rule
  stated as law, no scale in words. Correct, and unreadable at speed.
- `narration-with-skill.md` — fresh agent, same prompt, skill loaded: leads
  with the read, one number per sentence, every adjective carries its tell,
  ends on expectation + invalidation. Every context claim verified against the
  sheet (first visit to 7677 since the 08:30 bar; 27.75 pts high→low; 80% of
  7676's session volume in the last five minutes).

Prompt used for both (identical apart from the skill instruction):
"You are an orderflow analyst narrating the ES futures tape for a discretionary
trader who is watching the screen with you. It is 2026-08-24, 10:43 Central.
[fact-sheet field description] Read the file, then write the narration you
would give the trader right now about what the tape is doing and what it
means. You know nothing after 10:43. Return only the narration text."

To re-test after editing the skill: run the same prompt through a fresh
general-purpose agent with the skill loaded and grade against the six moves
and the self-check in SKILL.md.

## 2026-09-18 — edits pending re-test (Steve: hold the test for now)

Added after Steve's review: (1) the scenario lookup table deriving inference /
expectation / invalidation from the first three moves; (2) comparison-set rules
for scale — day so far qualified by the day's character, local references over
whole-session ranks, cross-day references name their day type, detector events
are prompts not verdicts; (3) grade-in-prose under editorial license; (4) the
input contract, which drops percentiles from the fact sheet. **Untested**: the
planned re-test is the same day at 14:00 CT, where developing percentiles are
most misleading, and `episode_factsheet.py` needs the percentile fields removed
and day-character / running-maxima-by-side fields added first.

## 2026-09-18 — this fixture is no longer the only one [dr-22w.4]

`../episodes/` holds nine episodes covering all four rows of the scenario table
plus a null, built by a generalized fact-sheet builder on the revised input
contract (no percentiles; day character; running maxima by side). Four of the
eight scenario episodes go the read's way and four do not. Re-tests should run
against that set; this directory stays as the RED/GREEN record.

Two corrections to what is here, found while building it:

- The overnight range quoted in `briefing-1043.md` was a midnight-to-open range
  labelled as a 17:00 open. The true 2026-08-24 overnight high is 7703.25, not
  7686.5 (the low, 7664.5, is right). `episode-facts.json` is left as issued —
  it is what the narrators were handed — and the briefing now carries the
  correction inline. **Both narrations cited it**: the baseline names "7686.50
  overnight high" as a target above, and the skilled one says "the overnight
  high is nine and a half points up." It is 26.25 points up. Neither narrator
  could have known; the error entered through the fact sheet and passed
  untouched through both the narration and the grading. That is the argument
  for the input contract being a build step with its own tests, and it is why
  the new builder records the window each overnight range was measured over.
- The percentile fields this fixture carries are the ones the revised contract
  drops, and `../episodes/README.md` records why they are worse than they look:
  the 10:41–42 bars rank at effort 84.7 / 90.4 only because the ranking sample
  starts at the prior 17:00. Against the RTH session they rank 26.1 and 54.5.
