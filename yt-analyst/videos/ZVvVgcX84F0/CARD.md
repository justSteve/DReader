# Video: ZVvVgcX84F0

- **URL:** https://www.youtube.com/watch?v=ZVvVgcX84F0
- **Title:** Trading Like A Pro: The Wide Butterfly Spread Technique (on-screen episode title: "Cherry Bomb: The Butterflies Inside Your Butterfly")
- **Channel:** tastylive — host Tom Preston
- **Uploaded:** 2026-08-26 · **Duration:** 10:58 (658 s)
- **First analyzed:** 2026-08-28
- **Status:** closed

## Findings
_(curated by Claude Code: verified findings with timestamps)_

**Thesis.** A wide butterfly is a stack of one-step butterflies. Count them by
squaring the number of strike steps per wing; harvest each embedded fly as the
index crosses its center strike. Banners: 00:08 "A butterfly pays most at the
center strike"; 03:48 "A wide butterfly is made of one-step butterflies";
04:24 "Square the strike steps to count the butterflies"; 05:09 "Capture each
embedded butterfly at its peak"; 10:23 "If you trade butterflies, this is worth
knowing".

**Decomposition table (00:50–03:50).** Slide "Butterfly Overlays": 25/35/45 fly
(+1/−2/+1) = 1× 25/30/35 + 2× 30/35/40 + 1× 35/40/45. Row sums 25→1,
30→(−2+2)=0, 35→(1−4+1)=−2, 40→(2−2)=0, 45→1. Host walks each row aloud
02:50–03:39. 2 steps/wing → 2² = 4 embedded flies. **Verified: arithmetic**
(all five rows reproduce the original) and a 5-run transcription at 1 fps and
5 fps agreed on every cell.

**Live SPX trade (05:40–10:20), tastytrade platform.**
- Position already held (BTO/STO tags on the chain): SPX 0DTE **Aug 25 2026**,
  +1 7660P / −2 7675P / +1 7690P. SPX 7668–7669 during the demo.
  **Verified: frames** (`frames-552-600/f_0001,4,8.jpg`).
- Host's "$6.50" (05:46) is the live **MID** of the fly at 05:59 (bid 6.25 /
  mid 6.50 / ask 6.80), not the ticket limit. The ticket itself reads Limit
  7.60, Max Profit 740, Max Loss −760 (stale limit; 15 − 7.60 = 7.40 ✓).
  **Verified: frames** — this overturned Gemini's claim of "Limit −6.50, Max
  Profit 850, Max Loss 650" (see Lessons).
- Count (06:01–06:36): 15-pt wings ÷ 5-pt strikes = 3 steps → 3² = **9**
  embedded flies: 1× 60/65/70, 2× 65/70/75, 3× 70/75/80, 2× 75/80/85,
  1× 80/85/90 (1+2+3+2+1 = 9). **Verified: arithmetic.**
- Embedded values (07:06–08:00): ATM 7665/7670/7675 ≈ $0.95–1.00; OTM
  7675/7680/7685 ≈ $0.55; 7645/7650/7655 ≈ $0.65. Recomputed from chain mids
  in frames: ATM fly 0.88–1.00, 7675/80/85 fly 0.55 exactly. **Verified:
  frames + arithmetic** (7645 strike is off-screen; $0.65 unverified).
- Method (08:16): SPX → 7665, sell the two 7660/7665/7670 flies at peak;
  SPX → 7675, sell the 7670/7675/7680 fly. Edge ≈ $1.00 peak vs $0.55–0.65
  off-center. **Unverified** (spoken; no on-screen figure to check).

**Corrections to Gemini's read (pixels are the tiebreaker):**
1. Year: Gemini said "Aug 25 '25"; platform header reads 8/25/2026.
2. Ticket figures 850/650/6.50 were derived from the spoken $6.50, not read
   from the ticket (740 / −760 / 7.60 on screen).

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-08-28 (v0.2, pre-card)** — Aim: map the video and verify its numbers.
  Wide pass (60,165 tok) + two zooms (00:35–03:50, 05:30–10:30) + two frame
  pulls (05:52–06:00, 07:03–07:10). Verdict: content mapped; arithmetic
  checks all pass; two Gemini claims overturned by frames (year, ticket
  figures). Runs migrated to `runs/20260828-095240` (wide), `-095325`
  (table), `-095353` (platform). Frames kept as evidence: `frames-552-600/`,
  `frames-703-710/`.
- **2026-08-28 (v0.3 deploy)** — Aim: controlled `--fps`/`--resolution`
  comparison on 01:00–02:00 (5 runs, `runs/20260828-1016*`–`-1019*`) and
  verify the frames fix. Verdict: fps works, resolution inert (LESSONS.md);
  frames fix verified on 09:10–09:15 (test frames pruned). Card closed.

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- tastylive format: lower-third banner text states each segment's thesis
  verbatim — Gemini transcribes these reliably; they're a free outline.
- Dense data lives in two places: the education slide (~00:50–03:50, table on
  a dark background) and the tastytrade web platform (~05:40–10:20).
- Platform header carries the wall clock (8/25/2026 12:21 CDT) — use it to
  verify dates; the order ticket omits the year.
- On the tastytrade ticket, **Limit Price can be stale**; the live price is
  the BID/MID/ASK strip at the bottom of the order panel, which the host
  reads aloud. Max Profit/Loss are computed from the Limit, not the MID.
- Chain shows ~13 strikes (7650–7710) at the 40-strike view; strikes below
  7650 scroll off — plan frame pulls accordingly.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260828-101645 [01:00-02:00] gemini-flash-latest (tok 5699/716) — Q: Transcribe every number visible in the on-screen table verbatim. — runs/20260828-101645/
- 20260828-101754 [01:00-02:00] gemini-flash-latest (tok 21539/1464) — Q: Transcribe every number visible in the on-screen table verbatim. — runs/20260828-101754/
- 20260828-101845 [01:00-02:00] gemini-flash-latest (tok 5699/635) — Q: Transcribe every number visible in the on-screen table verbatim. — runs/20260828-101845/
- 20260828-102009 [01:00-02:00] gemini-flash-latest (tok 21539/882) — Q: Transcribe every number visible in the on-screen table verbatim. — runs/20260828-102009/
- 20260828-102108 [01:00-02:00] gemini-flash-latest (tok 5699/781) — Q: Transcribe every number visible in the on-screen table verbatim. — runs/20260828-102108/
