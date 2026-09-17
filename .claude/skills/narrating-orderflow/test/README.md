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
