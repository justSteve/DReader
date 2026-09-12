# LESSONS — discord-reader

Tool- and Gemini-level lessons; capture-specific observations go in that
capture's CARD.md. Entries: date, status (suspected | confirmed | decided),
lesson. Confirmed twice (or decisively once) → promote into CLAUDE.md, mark
`promoted`.

## Decisions

- 2026-08-28 decided — Paging (PgDn + ~1s hold) is the capture doctrine;
  scrolling demoted to legacy fallback. Rationale: easier on the operator
  (deciding factor, Steve's ruling), plus predicted advantages in frame
  legibility (static text vs motion blur + codec artifacts), guaranteed
  coverage (every message fully visible on ≥1 held page), tractable dedup
  (failure surface shrinks to page seams), and automatability (a paging
  macro is trivial; a controlled scroll is not). Prediction untested vs
  scroll by design — revisit only if paged transcripts underperform.
  `promoted` (CLAUDE.md capture procedure)

## Inherited from yt-analyst (2026-08-28, treated as confirmed here)

- Gemini's `uncertainties` field is honest about illegibility — but not
  about extrapolation: it will present inferred content as on-screen text
  (invented a year from a partial date; derived ticket figures from a
  spoken price). Pixels are the only hard verifier.
  `promoted` (CLAUDE.md verification doctrine)
- Internal-coherence checks verify consistency, not provenance.
- 503 spikes on gemini-flash-latest; script retries and falls back to
  gemini-2.5-flash automatically.
- Credential doctrine: GEMINI_API_KEY in project .env; ambient
  GOOGLE_API_KEY is evicted by the script.
- yt-analyst finding, relevance here unknown: on the YouTube-URL ingestion
  path, --fps works but --resolution is inert (served pre-sampled at low
  res, ~66 tok/frame). The UPLOADED-file path (ours) may honor both knobs.

## Verdicts — first ingest, 2026-09-12 (InvestiTrade #lessons, 21 s, ~5 pages; dr-vm0)

- 2026-09-12 confirmed — On the uploaded-file path the default sampling IS
  low res: 3,308 prompt tokens for 20.9 s at 2 fps ⇒ ~63 tok/frame after
  audio, and `media_resolution=LOW` returns the identical count. `HIGH` gives
  11,624 (~261 tok/frame). So the resolution lever is real here, unlike the
  YouTube-URL path. Verdict relayed to yt-analyst/LESSONS.md.
- 2026-09-12 confirmed — Resolution is a fidelity knob, not just a cost knob.
  Same clip, default res: 4 of 5 timestamps confabulated, the thread's
  opening message replaced by a phantom "Pinned a message.", "(edited)" read
  as "(valid)", one word wrong, one line dropped, no reply headers seen. High
  res: all correct; residual errors were two header emoji and one missing
  reply_to. `dread.py` now defaults to `--resolution high`. `promoted`
  (dread.py default; CLAUDE.md invocation notes)
- 2026-09-12 confirmed (n=1) — 2 fps + 1 s holds: zero message loss, zero
  seam duplicates, zero fragments over ~5 pages. Keep running the seam check;
  one capture is not a rate.
- 2026-09-12 confirmed — Game Bar records the focused Discord window cleanly
  at 1920×1032 / 30 fps. Its Captures folder on this box is OneDrive-
  redirected: `/mnt/c/Users/steve/OneDrive/Videos/Captures` (the documented
  default path does not exist). Set via `DREAD_CAPTURE_DIR` in `.env`.
- 2026-09-12 suspected — Embedded images can still be a blurred placeholder
  after a 1 s hold (one of four images here never loaded). Gemini at high res
  reports "Unloaded image placeholder" honestly. If the image content matters,
  hold that page ~2 s. Argues against the 0.5 s-hold idea for image-heavy
  channels.
- 2026-09-12 suspected — Emoji at the head of a message and reply-preview
  headers are the weakest reads even at high res (🟢/🔴 read as 🟥; one of
  three reply links missed). Spot-check both from frames when load-bearing.

## Open questions (standing diagnostics)

- 2026-08-28 suspected → confirmed n=1 (Verdicts above) — 2 fps + 1s page holds yields ≥1 clean sample per
  page and zero message loss. Verify on first ingests by grading a
  known-small section against the live channel.
- 2026-08-28 suspected — Seam failures (double-transcription of a message
  visible on two pages; boundary-straddling message split into fragments)
  occur at some rate. Run the seam check every ingest until the rate is
  known; if persistent, the fix is more prompt structure or a slightly
  longer hold, in that order.
- 2026-08-28 suspected → confirmed (Verdicts above) — fps/resolution knobs both apply on the uploaded-file
  path. Verify from an early ingest's token count against
  seconds × (per-frame-rate · fps + audio ~32/s): ~66/frame would mean
  low-res like YouTube; ~258/frame means default res and a real resolution
  lever. Report the verdict back to yt-analyst's LESSONS too.
- 2026-08-28 suspected → confirmed (Verdicts above; folder is OneDrive-redirected) — Game Bar (Win+Alt+R) records the focused window
  reliably for Discord. If it refuses or captures the wrong surface,
  fallback is OBS with a hotkey writing to the same watched folder.
- 2026-08-28 suspected — 0.5s holds would halve capture time and tokens at
  some loss risk. Only worth testing after 1s cadence shows zero loss.
