# LESSONS — yt-analyst

Tool- and Gemini-level lessons only; video-specific observations go in that
video's CARD.md. Each entry: date, status (suspected | confirmed), lesson.
Promotion rule: confirmed twice (or decisively once) → fold into CLAUDE.md
doctrine and mark the entry `promoted`.

- 2026-08-28 confirmed — YouTube URLs must be quoted in the shell (`&` splits
  the command) and stripped to bare `watch?v=ID` (playlist params confuse
  targeting). v0.3 canonicalizes the URL itself; quoting still required.
  `promoted` (CLAUDE.md Invocation)

- 2026-08-28 confirmed — Gemini's `uncertainties` field is honest: it declined
  fine-print axis labels rather than inventing them. Don't pressure it to
  guess; pull frames for illegible content. `promoted` (CLAUDE.md Trust)

- 2026-08-28 confirmed — Arithmetic cross-checks are a cheap, strong verifier:
  transcribed trading numbers satisfied points × contracts × $50 = P&L and
  P&L / risk = realized R to the cent. Hallucinated digits don't do
  arithmetic. `promoted` (CLAUDE.md doctrine step 3)

- 2026-08-28 confirmed — `gemini-flash-latest` threw 503 (high demand) on
  free tier; pinning `gemini-2.5-flash` worked immediately. Script now
  retries with backoff and falls back automatically. `promoted` (v0.2 code)

- 2026-08-28 superseded (see fps entry below) — `--fps` / `--resolution` may be inert for YouTube-URL
  ingestion: a ~70s window at nominal 5fps/high cost ~22.3K prompt tokens,
  consistent with default 1fps/default resolution. Diagnostic: run the same
  window with and without the knobs and compare `[tokens: ...]` lines.
  Consequence if confirmed: accuracy achieved so far is at the CHEAP sampling
  rate; knobs only matter for downloaded-file ingestion (not yet built).

- 2026-08-28 confirmed (2nd observation below) — Claim timestamps are approximate (± a few seconds);
  pad frame-pull windows ±10s when verifying a claim at t. Confirm against a
  few frame pulls before promoting.

- 2026-08-28 amended (see below: ~100/s observed) — Whole-video default-res passes run ~300 tokens/sec of
  video; clipped windows are near-free. Full analyzed video ≈ $0.03 on Flash.
  Cost shape: one wide pass per video, then unlimited cheap zooms.
  `promoted` (CLAUDE.md doctrine steps 1-2)

- 2026-08-28 promoted — `--fps` WORKS; `--resolution` is INERT for YouTube-URL
  ingestion. Controlled comparison, same 60s window (ZVvVgcX84F0 01:00-02:00,
  same question, 5 runs): default 5,699 = `--resolution low` 5,699 =
  `--resolution high` 5,699; `--fps 5` 21,539 = `--fps 5 --resolution high`
  21,539. Fits tokens ≈ seconds × (66·fps + 32) — Gemini's LOW per-frame rate
  plus audio — so URL ingestion samples at low resolution and the resolution
  knob cannot raise it; fps scales cost linearly. Accuracy: 1 fps transcribed
  every cell of the overlay table correctly; 5 fps produced more fragmented
  claims, not more correct ones. Supersedes the 2026-08-28 `suspected` fps
  entry above (now `superseded`). Runs: videos/ZVvVgcX84F0/runs/20260828-1016*
  to -1019*. PROPOSE CLAUDE.md: drop `--resolution` from doctrine; note fps.

- 2026-08-28 promoted (amends "~300 tokens/sec") — At default knobs this
  video cost ~92-95 prompt tokens per second of video across every shape:
  wide pass 658s → 60,165; 195s zoom → 18,035; 300s zoom → 27,639; 60s →
  5,699. The ~300/s figure is Gemini's documented default-resolution rate;
  YouTube-URL ingestion evidently bills at the low-res rate (see fps entry).
  Budget ~100 tok/s at default, ~360 tok/s at `--fps 5`. Full 11-minute video
  ≈ 60K tokens. PROPOSE CLAUDE.md doctrine step 2: "~100 tokens/second".

- 2026-08-28 promoted (amends arithmetic lesson) — Arithmetic consistency
  proves a number SET is coherent, not that it was READ OFF SCREEN. Gemini
  reported the tastytrade ticket as "Limit -6.50 db, Max Profit 850, Max Loss
  650, Net Debit 650" (kind: visual). Frames showed Limit 7.60 / Max Profit
  740 / Max Loss -760; the $6.50 was the live MID the host read aloud. Gemini
  derived 850/650 from the spoken 6.50 (15-wide fly: 15-6.50=8.50) and
  presented them as on-screen values. Derived numbers pass arithmetic checks
  by construction. Rule: arithmetic verifies internal consistency; PROVENANCE
  (on-screen vs spoken vs computed) needs frames whenever the claim is
  `onscreen_text`/`visual` and load-bearing. PROPOSE CLAUDE.md doctrine step 4
  amendment. Evidence: videos/ZVvVgcX84F0/frames-552-600/f_0004.jpg, f_0008.jpg.

- 2026-08-28 suspected — Gemini completes PARTIAL on-screen text with plausible
  defaults, dates especially. Ticket showed "Aug 25" (no year); Gemini reported
  "expiring Aug 25, 2025" / "Aug 25 '25". Platform header (8/25/2026) proved
  2026. Treat any year, unit, or suffix that isn't literally in `verbatim` as
  a guess; cross-check dates against a second on-screen source (platform
  clock, chart axis). Confirm on a second occurrence before promoting.

- 2026-08-28 confirmed — Claim timestamps: second observation. Ticket claim at
  05:54 matched frames 05:52-05:59; "index at 7669" at 07:06 matched frames
  07:03-07:10. Accurate to ±5s; ±10s padding is sufficient. `promoted`
  (already in CLAUDE.md Trust calibration).

- 2026-08-28 resolved — `frames` failed with ffmpeg exit 254: yt-dlp appends
  the merged container's extension to a hardcoded `-o clip.mp4` template
  (→ `clip.mp4.webm`) when the selected streams aren't mp4. Fixed [dr-bot]:
  `-o clip.%(ext)s` then glob `clip.*`; applied to v0.2 (64f8bd9) and
  re-applied to v0.3 on deploy [dr-dji]. Verified: 5s window → `clip.webm`
  → 5 frames.

- 2026-08-28 confirmed — Asking for VERBATIM transcription across a whole
  long video trips Gemini's RECITATION filter: `finish_reason=RECITATION`,
  `resp.text=None`, 119K prompt tokens billed, nothing returned (QaNPAaEnB5E,
  21 min). Same video, same question reworded "in your own words / paraphrase
  (do not transcribe speech)" → full answer. Rule: wide passes ask for
  paraphrase + structure + dense-data timestamps; "verbatim" only on clipped
  windows (1-3 min), where it has never tripped. v0.3 now reports
  finish_reasons instead of crashing on an empty response [dr-08s.9].
  PROPOSE CLAUDE.md doctrine step 2: add "paraphrase, never verbatim, on the
  wide pass".

- 2026-08-28 promoted — Default 1 fps sampling is the doctrine default: in the
  same 5-run comparison it read every table cell correctly while `--fps 5`
  fragmented claims without improving accuracy. `--fps` is reserved for
  genuinely fast-moving content, not used as a quality knob. Approved by
  Steve with the three entries above (CLAUDE.md "Sampling knobs").

- 2026-08-28 suspected — LABEL FUSION: Gemini merged two spatially separate
  chart labels into one string. Chart showed `15m ($5771)` (top right) and
  `RESISTANCE ($5730)` (bottom right); Gemini reported one label
  "RESISTANCE (1515m)" — a string that exists nowhere on screen, with both
  dollar figures dropped. Any `verbatim` that looks like a composite (two
  units, a parenthetical that doesn't parse) is a candidate fusion; pull
  frames. (QaNPAaEnB5E 16:59; Opus verifier, frames-1655-1750/f_0002.jpg)

- 2026-08-28 suspected — TRUNCATION AT OCCLUSIONS presented as complete:
  "Daily Avg: 1,475" was `Daily Avg: 1,475,6…` cut off by the webcam bubble —
  a ~1.47M volume figure reported as 1,475 with no uncertainty flag. Pairs
  with the partial-text COMPLETION lesson (dates): Gemini neither flags
  partial text as partial nor its completions as guesses. Numbers adjacent
  to an overlay (webcam, cursor, drawing) need frames. (QaNPAaEnB5E 16:59)

- 2026-08-28 suspected — FABRICATED JUSTIFICATION inside `uncertainties`:
  Gemini wrote "ticker partially occluded by red text" when no header was in
  frame at all (crop starts below it) and no red text existed at that
  timestamp. The uncertainty itself was honest (ticker unknown); the stated
  REASON was invented. Trust the flag, not the explanation. (QaNPAaEnB5E)

- 2026-08-28 suspected — NARRATION ORDER ≠ CHART CHRONOLOGY: Gemini's
  paraphrase followed the presenter's speaking order (resistance rejection →
  selloff → support bounce) but on the chart the support bounce is at the
  far left, before the rally. Paraphrases of chart walkthroughs describe the
  narration; do not read them as a time sequence without frames.
  (QaNPAaEnB5E 17:05–17:58)

- 2026-08-28 confirmed — Opus subagent as second reader works: one
  general-purpose Opus agent, read-only, given run dirs + frame dirs + a
  numbered checklist, returned a per-item AGREE/DISAGREE report with frame
  paths in ~6.5 min / ~90K tokens, caught all four findings above, and kept
  ~30 JPEGs out of the parent context. Give it the claim list and the
  frame→timestamp formula; ask for "additional on-screen text not reported".
