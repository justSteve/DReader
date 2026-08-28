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

- 2026-08-28 confirmed (see glyph-confusion entry) — LABEL FUSION: Gemini merged two spatially separate
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

- 2026-08-28 confirmed — WIDE-vs-ZOOM DISAGREEMENT, arithmetic as tiebreaker
  before frames: on the same trade log the wide pass read $18,750 / 8.33R and
  the zoom read $14,750 / 6.33R. Only the wide set closed four independent
  equations (P&L, planned R, realized R, target distance); frames confirmed
  it. Two runs on the same screen are a free consistency check — when they
  differ, arithmetic usually picks the winner and frames confirm.
  (eJZhX6Xz4cU 17:26)

- 2026-08-28 suspected — DENSE NUMERIC GRIDS: Gemini misread 4 of 21 cells on
  a footprint ladder (e.g. `9×45` → `17×27`, `886×972` → `890×813`) while
  getting the other 17 exact and every slide sentence word-perfect. Per-cell
  error ~20% on 3-4 digit numbers packed at ~12px. Cheap structural checks
  for footprint data: delta = ask − bid, and delta ≡ total volume (mod 2).
  Otherwise frames. (eJZhX6Xz4cU 08:08; Opus verifier)

- 2026-08-28 suspected — COLOR ATTRIBUTION is weaker than text: one Time &
  Sales row Gemini called red reads green in two frames (Opus). Where color
  carries meaning (buy/sell, positive/negative delta), verify by pixels or by
  the number's sign, not by Gemini's color word. (eJZhX6Xz4cU 07:53)

- 2026-08-28 confirmed — Gemini reliably tags spoken-only settings as
  `spoken` rather than inventing on-screen text for them ("Sierra Chart",
  "20 tick / 5 point range" — no settings panel ever appeared). The `kind`
  field is trustworthy for provenance at the claim level; the failure mode
  is derived NUMBERS labelled `visual`, not spoken words labelled `onscreen`.

- 2026-08-28 confirmed (2nd observation) — LABEL FUSION recurs: `RESISTANCE
  ($5730)` reported as "RESISTANCE (151759)" (0QlGCz6U_1g 05:25), after
  "RESISTANCE (1515m)" in QaNPAaEnB5E. Same channel, same label style
  `NAME ($price)`. Any parenthetical that isn't a clean `$dddd` is a misread;
  the dollar sign is dropped every time. Pull frames for zone labels.

- 2026-08-28 suspected — PROGRESSIVE SLIDE BUILDS get collapsed: the wide
  pass reported a six-bullet slide at 07:07 when only the header was on
  screen; the full list appeared by 09:39. A wide-pass timestamp for a slide
  marks first appearance; verbatim text may come from minutes later. When
  order/timing matters, zoom the window and ask when each bullet appears.

- 2026-08-28 suspected — WRONG-TAB INSTRUMENT: Gemini reported "NQZ4 (CME)"
  from an inactive Bookmap tab while the displayed chart was ES (axis
  5733–5754; NQ was ~20,000). Also appended "250 Vol" that was not visible.
  Sanity-check any instrument read against the price axis.

- 2026-08-28 suspected — TIMESTAMP FIELDS: `10:03:39.368 (EDT)` became
  "10:03:39 PM EDT (+00)" — milliseconds reinterpreted as meridiem/offset.
  Treat clock strings as approximate to the second; don't trust AM/PM or
  timezone suffixes without frames.

- 2026-08-28 suspected — WIDE PASS SKIPS SEGMENTS: a ~55 s chart segment
  ("Buying every single move up or down", 06:10–07:06) was absent from the
  wide pass's 13 claims; the verifier found it in a frame pulled for the
  next slide. The wide pass is a sample, not a table of contents — cheap
  insurance is one extra zoom over any gap > 60 s between claims.

- 2026-08-28 confirmed — ARITHMETIC ON HISTOGRAMS: the verifier transcribed
  ten bar values from a Goldman daily-P&L chart and they summed to the
  slide's headline figures (236 / 112 / 41) — structural checks work for
  charts as well as trade logs; hallucinated bars don't sum.

- 2026-08-28 confirmed (3rd observation, root cause) — The "label fusion"
  pattern is a GLYPH CONFUSION: Gemini reads the pair `$5` as `60`.
  `0p ($5806)` → "Tp (6080)"; `15m ($5771)` → "15m (60775)"; `RESISTANCE
  ($5730)` → "RESISTANCE (60720)" (00QtD-RosLg 06:55, checked directly);
  earlier "RESISTANCE (1515m)" / "(151759)" are the same confusion plus
  neighbour bleed. Expect it on any `$5xxx` price label at small font (ES
  prices in 2024–25 all start with 5!). Rule: a parenthetical price on this
  channel's charts is only trusted from frames. Marking the two earlier
  `suspected` fusion entries `confirmed` under this root cause.

- 2026-08-28 confirmed (3rd observation) — DENSE GRID error rate holds:
  5 of 21 rows wrong on a clean, high-contrast bid×ask ladder (00QtD-RosLg
  09:13; errors include swapped rows, invented 1466×2315, dropped 1157×1409,
  and a wrong row count "20"). Combined with eJZhX6Xz4cU (4/21) the rate is
  ~20–25% per row regardless of legibility. Grids > ~10 rows: frames only.
  PROPOSE CLAUDE.md: add to doctrine step 3 — "never take a ladder/table
  > 10 rows from Gemini alone; pull frames".

- 2026-08-28 suspected — `$` GLYPH → "1": journal input boxes showing
  `$ 5631.0` were transcribed "1 5631.0" by both the wide pass and a zoom
  (5qBo04SMUFc 25:36). Sibling of the `$5`→`60` confusion: the dollar sign
  at small size is unstable. Strip/ignore a stray leading "1 " before a
  price and check frames when the `$` matters.

- 2026-08-28 confirmed — PRIOR-KNOWLEDGE LEAK: the wide pass named the
  channel "InvestiTrade" (5qBo04SMUFc) and "Invest Trade" (7facFfjQ0UE);
  no such wordmark exists on screen in either (verifier + direct check).
  Names, brands and affiliations in a `summary` are not transcription —
  only `verbatim` fields with frame backing count for identity claims.

- 2026-08-28 suspected — ADJACENT-ROW BLEED on footprints: Gemini reports
  the top cell correctly (29/29, 136/136, 51/51) then invents the row below
  as a copy of a nearby number ("131/131", "141/141") where the real rows
  are 333/491 and 61/147. Trust the FIRST cell it names at an extreme;
  treat "followed by …" continuations as unverified.

- 2026-08-28 confirmed — PARITY CHECK IS DECISIVE for footprint cells: a
  Gemini "−583" beside volume 1498 is impossible (delta = ask − bid and
  volume = ask + bid share parity); pixels read −538 (w7tvJCuZAq8 27:18).
  Run delta ≡ volume (mod 2) on every cited cell before frames; a parity
  failure is a transcription error with certainty. `promoted` candidate
  for doctrine step 4 (structural checks) — PROPOSE CLAUDE.md.

- 2026-08-28 suspected — CROSS-CHART BLEED: the price axis Gemini gave for
  the 03:19 chart (5645–5690) belongs to the footprint shown minutes later
  (5648–5664); the real axis was 5850–5935. In a multi-chart segment,
  attribute axes/levels to a chart only from a frame at that timestamp.

- 2026-08-28 suspected — SPOKEN ROUND-OFFS become values: "1700 / +1300"
  (on screen 1775 / +1319) and "1200" (1245) were reported as the
  figures. When a claim is `spoken`, the number is the presenter's
  rounding; the on-screen cell is the record — pull it.

- 2026-08-28 confirmed (2nd observation) — Slide/bullet timestamps run
  2–4 s early: Gemini stamps a slide at the moment its title appears, but
  bullets animate in afterwards (w7tvJCuZAq8 16:39→16:43, 23:25→23:29;
  0QlGCz6U_1g 07:07→09:39). Pad frame pulls +5 s after a slide timestamp.

- 2026-08-28 confirmed (2nd observation) — WIDE-vs-ZOOM disagreement,
  arithmetic first: on tgQC7Dpcc8A trade 1 the WIDE pass was wrong
  (−$2,600 / 5.96R) and the zoom right (−$2,625 / 5.86R) — the reverse of
  eJZhX6Xz4cU. Neither shape is privileged; the closing set wins, frames
  confirm. Also: a DOM row VPS 1937 / VPB 3570 / VPD 1633 / SVP 5507 closes
  both column identities (difference and sum) — a live ladder row is a
  free two-equation check.

- 2026-08-28 suspected — DECORATIVE GLYPHS INVENTED: Gemini rendered the
  journal's `$` input-box prefixes as "↑ 5820.0" / "↓ 5808.5" (arrows that
  don't exist), after reading the same prefix as "1" elsewhere. Any
  symbol adjacent to a number in `verbatim` is suspect; the digits are
  usually right.

- 2026-08-28 confirmed — SUBAGENT HYGIENE: one Opus verifier hung ~60 min
  on an API error with zero output; the retry with "do item 1 FIRST, keep
  under ~25 tool calls" finished in 33 min. Give verifiers an explicit
  priority order and a call budget, and nudge after 30 min of silence.
