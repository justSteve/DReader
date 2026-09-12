# discord-reader — operating instructions for Claude Code

You drive `dread.py`, which turns Steve's screen-captured page-throughs of
Discord into structured transcripts via Gemini Flash. Gemini is the eyes; you
are the analyst and archivist. Sibling project to ../yt-analyst — same
doctrine, different source.

## Capture procedure (Steve's side — for reference when he asks)

Paging is the doctrine (ruled 2026-08-28); scrolling is legacy fallback.

1. Focus Discord, **click into the message pane** (so PageDown drives the
   channel, not a sidebar), navigate to the starting point.
2. **Win+Alt+R** starts Game Bar recording of the focused window.
3. **PageDown → hold ~1 second → repeat** until the endpoint. Never press
   Esc mid-capture (Discord jumps to newest). If an image/embed is loading,
   give that page an extra beat.
4. **Win+Alt+R** stops. MP4 lands in the Captures folder. On this box that
   folder is OneDrive-redirected (WSL: /mnt/c/Users/steve/OneDrive/Videos/
   Captures); `.env` sets DREAD_CAPTURE_DIR to it. If an image or embed is
   still a blurred placeholder, hold that page ~2 s (seen 2026-09-12).

Why 1 second: at 2 fps sampling it guarantees ≥1 clean static sample per
page even after Discord's page-transition animation. 0.5s cadence is a
possible future optimization — only after 1s has a proven loss rate of zero.

## Invocation

Run from this directory; activate the venv (`source .venv/bin/activate`) or
use `.venv/bin/python dread.py ...`. The API key loads automatically from the
vault file `/home/vault/DReader/env` — never ask for it, never echo it. It is
deliberately not in this tree and not in the shell: a value in a file always
beats one exported into the environment, so a stale exported key cannot shadow
the live one. If a call comes back unauthenticated, run
`.venv/bin/python dread.py env` — it names the file the key came from, prints
its length and a sha256 prefix (never the value), and makes one live call to
Google to say whether the key still works. `.env` beside the script is for
settings only, `DREAD_CAPTURE_DIR` among them; a secret placed there is
ignored with a message.

- Ingest newest capture:
  `dread.py ingest --label "server/channel"`
  (`--resolution high` is the default since 2026-09-12: at default/low res
  Gemini confabulated 4 of 5 timestamps and dropped a message on the first
  ingest; high costs ~3.5× the video tokens and read them all. `--resolution
  low` only for a cheap first look where timestamps do not matter.)
  (mode defaults to `page`; `--mode scroll` only for legacy captures. Moves
  the source into the dossier; `--keep` copies. Refuses a >30-min-old
  "newest" file unless `--yes` — that guard catches Game Bar having
  silently failed to record.)
- Follow-up on an ingested capture:
  `dread.py ask --capture <capture_id> --question "..."`

## Dossier layout

`captures/<capture_id>/` — capture_id is timestamp + slugified label.
- `CARD.md` — the dossier; dread.py creates it, appends one line per
  ingest/ask to the final `## Run log`. Everything above that is yours.
- `source.mp4` — ground truth, LOCAL: frame checks are one ffmpeg call
  (`ffmpeg -ss MM:SS -i source.mp4 -frames:v 1 check.jpg`).
- `transcript.json` / `transcript.md` — structured and readable output.
- `runs/<ts>/` — follow-up asks (sub-cards).

## Verification doctrine

Paging concentrates the failure surface at page seams. After every ingest:

1. **Seam check (the paged dedup check).** The known failure modes are a
   message transcribed twice because it appeared on two consecutive pages,
   and a boundary-straddling message transcribed as two fragments. Scan
   transcript.md for near-duplicate adjacent messages and mid-sentence
   splits. Found → fix the transcript, note in the card's Lessons.
2. **Continuity check.** Timestamps and date dividers monotonic; a backwards
   jump means a page was double-counted or misordered.
3. **Boundary check.** Confirm the transcript's first and last messages
   match the first and last held pages of source.mp4 (pull one frame from
   each end). Missing head/tail → capture started/stopped mid-sequence;
   note in card, tell Steve.
4. **Spot verification.** For any message that matters downstream, pull the
   frame where it's visible and compare pixels to transcript. Inherited
   lesson: Gemini presents inference as reading — verbatim fields are
   aspirations, pixels are ground truth. No arithmetic checks exist here;
   frames are the only hard verifier.
5. **Uncertainties are honest about illegibility** (not about extrapolation).
   Check flagged content against frames; if pixels are legible to you,
   transcribe it yourself and note that Gemini under-read.

## Card maintenance (end of every session)

- **Summary**: channel, date range, topic — once known.
- **Findings**: what was extracted/decided, with message refs (author+time).
- **Lessons (this capture)**: cadence problems, layout quirks, seam issues —
  recurring ones feed up to LESSONS.md.
- **Status**: `open` → `closed` when transcribed, verified, reported.
- Never edit `## Run log`.

## Lessons doctrine

Tool-level lessons to `LESSONS.md`, dated, `suspected`/`confirmed`; promote
into this file when confirmed — propose doctrine edits to Steve, don't apply
them unilaterally. Standing diagnostics are listed there; resolve them
opportunistically and record verdicts.

## Reporting conventions

- Translate; don't dump. Report: what the capture covers, message count,
  verification results, discrepancies (with frame refs), material
  uncertainties. Cite transcript.md and card paths; don't paste raw JSON.
- Transcript-vs-pixels discrepancies go to Steve with the frame path — he
  is the tiebreaker.

## Housekeeping

- `captures/*/source.*` are primary artifacts — never delete; transcripts
  hang from them. `runs/` is working data. CARD.md, transcript.md, LESSONS.md
  are the distilled knowledge (version-worthy if this becomes a repo).
- This is Steve's own Discord account viewed on his own screen — personal
  archival. Transcript contents are private working data: they stay in this
  directory and in reports to Steve.
