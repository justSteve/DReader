# Operating the orderflow practice episodes

Evergreen page — updated in place. Last revised 2026-09-18 (bead dr-22w.4).
Home: `DReader/.claude/skills/narrating-orderflow/episodes/`.

## What this is

Nine moments from Strader's tape, each frozen at a cutoff minute. One of them is
a complete exercise: give a narrator everything that was knowable at the cutoff,
read what it says, then check it against what actually happened. The set covers
the four scenarios in the skill's table twice over, plus one where nothing is
happening.

Everything here is read-only against Strader. The tape is read through one door
(`tape.py`) and nothing in this directory writes outside itself.

## The files in one episode

| file | what it is | who may see it |
|---|---|---|
| `facts.json` | everything observable at the cutoff | the narrator reads this |
| `briefing.md` | the same thing laid out for a person, with the prompt at the foot | you, if you want to try it yourself |
| `aftermath.json` | the 45 minutes after the cutoff | grading only |
| `detectors.txt` | what Strader's detectors emitted, run two ways | grading only |
| `key.md` | the scenario, the verdict, and why | grading only, and last |

## Running an episode

1. Start a fresh agent. Give it the skill and the episode's `facts.json`.
2. Give it the prompt at the foot of that episode's `briefing.md`. It is the
   same prompt for every episode and the same one the two 2026-08-24 narrations
   answered, so results stay comparable.
3. Grade what comes back against the six moves and the self-check in the skill.
4. Only then open `key.md`, and `aftermath.json` for the path.

Order matters. Reading the key first makes the exercise worthless. Reading the
aftermath first turns grading the *read* into grading the *outcome*. That is the
habit this set exists to break. Four of these episodes go against the correct
read.

## Grading

Grade the read, not the result. A good narration states the evidence. It says
who is on the wrong side. It ends on one thing to watch and one thing that would
prove it wrong. A narration like that is a pass even when the trade loses. A
narration that predicts and happens to be right is a fail.

Three things to check every time:

- **Scale.** Every size word has to name what it is big compared to. "The
  biggest sell minute of the day" is a claim the fact sheet can settle; "heavy
  selling" is not.
- **Tell.** Every strong word — absorbed, trapped, not getting paid — needs both
  halves in the same breath: the effort, and the result that contradicts it.
- **Ending.** The last two sentences are what to watch and what proves it wrong.

## Rebuilding

Use Strader's interpreter; it is the one with the tape libraries. Day files
cache under `.cache/` (ignored by git, about a second a day after the first
read).

```bash
S=/root/projects/Strader/.venv/bin/python
cd DReader/.claude/skills/narrating-orderflow/episodes

$S scan.py --start 2026-08-03 --end 2026-09-17 --top 10
$S factsheet.py --id ep01 --day 2026-08-26 --cutoff 09:28 --level 7680.5 --defends low
$S render.py ep01 > ep01/briefing.md
$S detectors.py --day 2026-08-26 --cutoff 09:28 > ep01/detectors.txt
```

`--defends low` means a buyer is holding the floor at that price. `--defends
high` means a seller is capping it. For the acceptance episodes, use the far edge
of the quiet stretch rather than the extreme of the move. When an upward move is
accepted, dips into the quiet area get bought. The read is wrong when that floor
gives way.

## Adding an episode

1. Run `scan.py` over the days you want. It scores candidates for each scenario
   and prints them by class.
2. Pick one and read it against the tape yourself. Every episode in the set was
   verified by hand before it went in — twice this caught the scanner naming a
   level that no price had traded at.
3. Build the fact sheet, the briefing and the detector readout with the commands
   above.
4. Write `key.md`: the scenario, what the tape showed, what the detectors said,
   what happened next, and the verdict.
5. Add a row to the set's README table.

The scanner's thresholds are a prompt to look, never a verdict. That is the
skill's own rule about detector output, and it applies to the tool that builds
its practice material.

## Rules the tools enforce, and why

**A day under half the recent median volume is refused.** The tape capture
stayed on the expiring September contract through 09-17 while trading had moved
to December: 09-16 holds 111,000 contracts against a million-contract norm, on a
122-point range. Holidays fail the same test. Without this guard the set would
have taken an episode from a dying market, and it nearly did.

**The overnight range spans two files.** A corpus day is a calendar day. The
session that opens at five in the evening sits in the previous day's file. Each
fact sheet states the window it actually measured. Some days are missing their
evening: 2026-08-31 is a Monday with no Sunday reopen. Some are missing
everything before the open, as 2026-08-03 is.

**Never walk back more than one day to find an evening session.** Doing so
labelled the previous Thursday evening as Monday's overnight range.

**Absorption is found by one-sided pressure, not by volume.** The known
2026-08-24 case is 0.9 and 1.1 times a normal minute — no surge at all. What
made it absorption was pressure at a level with nothing to show for it.

**Acceptance is read off raw minutes.** The zigzag leg-finder ends a leg at its
extreme only because price later turned. Taking the minutes after a leg end
therefore samples the start of the turn. The first version did that. It produced
seven candidates in two months and none of them continued.

**The fact sheet carries no percentiles and no cell names.** Both depend on
which hours are in the ranking sample. That choice moves the answer more than
the market does. The same minute reads dead against the trading session and
heavy against the overnight hours.

**Selection may use hindsight; the fact sheet may not.** Choosing which moment
to freeze is allowed to look at the whole day. Every field in `facts.json` is
causal to the cutoff. Never pick an episode by its aftermath alone — that is how
a set ends up teaching that absorption always works.

## When something breaks

| symptom | cause | fix |
|---|---|---|
| `no RTH prints` | a weekend or holiday file | skip it; the scanner already does |
| a day scanned but skipped as low volume | contract roll or half day | expected — see the volume guard above |
| a level that no price traded at | anchoring on the named level rather than the defended price | `--level` takes the price that was defended; the named level travels as context |
| the detectors disagree with the two runs | they are two different ranking samples, not a bug | report both, as `detectors.txt` does |
| `ModuleNotFoundError: market` | ran with the wrong interpreter | use Strader's `.venv/bin/python` |
