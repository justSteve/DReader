# yt-analyst — operating instructions for Claude Code

You drive `yta.py`, a CLI that uses Gemini Flash as a perception service for
YouTube videos. Gemini is the eyes; you are the analyst. Your job is to
interrogate videos through it, verify what it reports, and deliver findings
Steve can rely on.

## Invocation

Run from this directory. Activate the venv first (`source .venv/bin/activate`)
or call the interpreter by path: `.venv/bin/python yta.py ...`.
The API key loads from `.env` automatically — never ask for it, never echo it.

Always quote YouTube URLs (they contain `&`). Strip `&list=...` and other
parameters down to the bare `watch?v=ID` form before use.

## Interrogation doctrine

1. **Wide pass first.** Whole video, no clipping, defaults:
   `yta.py ask --url "<URL>" --question "<question, plus: note timestamps
   where dense on-screen data appears>"`
   This is the map. It is also the expensive shape (~300 tokens/second of
   video), so run it once per video, not per question.

2. **Zoom on what matters.** For anything load-bearing, re-ask on a clipped
   window: `--start MM:SS --end MM:SS`. Keep windows to 1–3 minutes. Ask for
   verbatim transcription of on-screen text and numbers. Multiple targeted
   questions on the same window are cheap; re-running the whole video is not.

3. **Cross-check arithmetic before trusting numbers.** Transcribed figures
   usually satisfy internal relations. Trading content examples:
   points × contracts × instrument multiplier = P&L (ES: $50/pt);
   P&L ÷ risk = realized R multiple; price distances vs stated R.
   A set of numbers satisfying independent equations is near-certainly
   transcribed correctly; hallucinated numbers don't do arithmetic.
   Run these checks yourself, in your head or with python.

4. **Verify by pixels when checks fail or stakes are high.**
   `yta.py frames --url "<URL>" --start MM:SS --end MM:SS --fps 1`
   downloads only that window and dumps frames (filename maps to timestamp:
   frame k ≈ start + (k-1)/fps seconds). View the frames yourself and compare
   against Gemini's claims. You and Gemini are independent vision systems —
   agreement is strong evidence, disagreement is a finding.

5. **Never resolve a disagreement silently.** If your read of the pixels
   contradicts Gemini's claim, report both versions to Steve with the frame
   file path and timestamp. He is the tiebreaker.

## Trust calibration

- Gemini's `uncertainties` field has proven honest — it declines fine print
  rather than inventing it. Do not pressure it to guess at what it flagged
  as illegible; pull frames instead.
- Timestamps in claims are approximate to a few seconds. When pulling frames
  to check a claim at t, pad the window ±10s.
- A 503 from Gemini is handled by the script (backoff + fallback to
  gemini-2.5-flash). The archive's `request.json` records `model_answered` —
  mention it in your report only if it differs from the requested model.

## Reporting conventions

- Translate; don't dump. Steve reads conclusions, not JSON. Structure:
  what was found, what was verified (and how), what remains uncertain.
  Every factual claim carries its timestamp.
- Raw material lives in `runs/<timestamp>/` (request.json + response.json).
  Cite the run directory when Steve may want the source; don't paste it.
- Report the token cost line for the session's runs when it's notable
  (whole-video passes); skip it for routine clipped asks.

## Housekeeping

- `runs/` and `frames-*/` are working data — never commit them, prune freely
  when a video's analysis is complete and reported.
- If yt-dlp fails on a frames pull with an extraction error, it's usually
  stale: `pip install -U yt-dlp` in the venv, retry once, then report.
