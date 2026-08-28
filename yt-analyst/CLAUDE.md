# yt-analyst — operating instructions for Claude Code

You drive `yta.py`, a CLI that uses Gemini Flash as a perception service for
YouTube videos. Gemini is the eyes; you are the analyst. Your job is to
interrogate videos through it, verify what it reports, maintain the dossier,
and deliver findings Steve can rely on.

## Invocation

Run from this directory. Activate the venv first (`source .venv/bin/activate`)
or call the interpreter by path: `.venv/bin/python yta.py ...`.
The API key loads from `.env` automatically — never ask for it, never echo it.

Always quote YouTube URLs (they contain `&`). The script canonicalizes URLs
to bare `watch?v=ID` form itself.

## Dossier layout

Every video gets a directory: `videos/<video_id>/`.

- `CARD.md` — the video's dossier. yta.py creates the skeleton on first
  contact and appends one line per run to the final `## Run log` section.
  Everything ABOVE that section is yours to curate (see Card maintenance).
- `runs/<timestamp>/` — raw request/response JSON for each ask (a sub-card).
- `frames-*/` — verification frames, colocated with their video.

## Interrogation doctrine

1. **Check the card first.** If `videos/<id>/CARD.md` exists, read it before
   asking Gemini anything — prior sessions may already hold the answer, and
   its Lessons section tells you this channel's quirks.

2. **Wide pass once.** Whole video, no clipping, defaults:
   `yta.py ask --url "<URL>" --question "<question, plus: note timestamps
   where dense on-screen data appears>"`
   This is the map and the expensive shape (~100 tokens/second of video —
   YouTube-URL ingestion bills at Gemini's low per-frame rate; an 11-minute
   video ≈ 60K prompt tokens). One per video, ever, unless the question
   demands a different wide framing. Defaults means defaults: no `--fps`,
   no `--resolution` (see Sampling knobs below).

3. **Zoom on what matters.** For anything load-bearing, re-ask on a clipped
   window (`--start MM:SS --end MM:SS`, keep to 1-3 minutes). Ask for
   verbatim transcription of on-screen text and numbers. Clipped follow-ups
   are near-free; run as many as the question needs.

4. **Cross-check arithmetic before trusting numbers.** Transcribed figures
   usually satisfy internal relations. Trading content examples:
   points × contracts × instrument multiplier = P&L (ES: $50/pt);
   P&L ÷ risk = realized R multiple. Numbers satisfying independent equations
   are near-certainly a coherent set; hallucinated numbers don't do
   arithmetic. Run these checks yourself. **But arithmetic verifies
   consistency, not provenance.** Gemini can DERIVE figures from a spoken
   number and report them as on-screen values (Cherry Bomb: "Max Profit 850 /
   Max Loss 650" computed from the host's "$6.50"; the ticket read 740 /
   −760). Derived numbers pass arithmetic by construction. When a claim is
   `onscreen_text`/`visual` and load-bearing, provenance needs frames.

5. **Verify by pixels when checks fail or stakes are high.**
   `yta.py frames --url "<URL>" --start MM:SS --end MM:SS --fps 1`
   downloads only that window and dumps frames (frame k ≈ start + (k-1)/fps
   seconds; pad the window ±10s around a claim's timestamp). View the frames
   yourself and compare against Gemini's claims. You and Gemini are
   independent vision systems — agreement is strong evidence, disagreement
   is a finding.

6. **Never resolve a disagreement silently.** If your read of the pixels
   contradicts Gemini's claim, report both versions to Steve with the frame
   file path and timestamp. He is the tiebreaker.

## Sampling knobs (YouTube-URL ingestion)

Measured 2026-08-28 (controlled 5-run comparison, LESSONS.md):

- **Default sampling (1 fps) is the doctrine default.** It read every cell of
  a dense table correctly; `--fps 5` cost 3.8× and fragmented the claims
  without improving them. `--fps` is not a quality knob — reserve it for
  genuinely fast-moving content (scrolling tape, rapid chart replays).
- **`--resolution` is inert on this path.** Gemini serves YouTube URLs
  pre-sampled at low resolution and the knob cannot raise it. The flag stays
  in the code: uploaded-file ingestion may honor both knobs.
- **Cost model:** prompt tokens ≈ seconds × (per-frame · fps + 32), where
  per-frame is 66 at low res and ~258 at default res. One token-count check
  against this formula tells you which rate any ingestion path is on.
- Upshot: the accurate configuration and the cheapest configuration are the
  same one.

## Card maintenance (end of every session)

Before finishing a session on a video, update its CARD.md:

- **Findings**: merge in what this session established, as timestamped
  prose. Mark each item verified (and how: arithmetic / frames / both) or
  unverified. Correct anything a later session overturned — the card states
  current best knowledge, not history (history lives in runs/).
- **Sessions**: append one short entry — date, what the session set out to
  answer, verdict, which runs it used.
- **Lessons (this video)**: anything peculiar to this video or channel —
  chart software, layout, recurring segment structure, where the dense data
  lives. Future sessions on this channel read this first.
- **Status**: flip `open` → `closed` when the video's questions are answered;
  a closed card can be reopened.
- Never edit the `## Run log` section — it is machine-appended.

## Lessons doctrine (tool-level)

When you learn something about the TOOL or GEMINI'S BEHAVIOR (not about a
particular video), append a dated entry to `LESSONS.md` with status
`suspected` or `confirmed`. When a suspected lesson is confirmed by a second
independent observation, mark it confirmed and propose the CLAUDE.md change
to Steve — lessons graduate into doctrine; they don't rot in the log.
Open items in LESSONS.md (e.g. the fps-knob question) are standing
diagnostics: resolve them opportunistically when a session's runs happen to
produce the comparison, and record the verdict.

## Trust calibration

- Gemini's `uncertainties` field has proven honest — it declines fine print
  rather than inventing it. Do not pressure it to guess; pull frames instead.
- Claim timestamps are approximate to a few seconds; pad frame windows.
- 503s are handled by the script (backoff + fallback to gemini-2.5-flash).
  The run log and request.json record `model_answered`; mention it in your
  report only if it differs from the requested model.

## Reporting conventions

- Translate; don't dump. Steve reads conclusions, not JSON. Structure:
  what was found, what was verified (and how), what remains uncertain.
  Every factual claim carries its timestamp.
- Cite the card path and run directories when Steve may want the source;
  don't paste raw JSON.
- Report token cost only when notable (wide passes); skip for routine zooms.

## Housekeeping

- `videos/*/runs/` and `videos/*/frames-*/` are working data — never commit
  them. CARD.md and LESSONS.md ARE worth versioning if this directory is a
  repo: they're the distilled knowledge.
- Prune a video's frames-* directories once its card is closed; keep runs/.
- If yt-dlp fails on a frames pull with an extraction error, it's usually
  stale: `pip install -U yt-dlp` in the venv, retry once, then report.
