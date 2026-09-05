# Trade Brigade newsletter — call grading

Grades Matt's Sunday "Trade Brigade" newsletter (newsletter@tradebrigade.co,
in Steve's Gmail since 2024-07-25) against what the market then did. Built
2026-09-05 under bead dr-4ne to answer one question: when the letter says
something checkable, how often is it right, and is that better than a coin or
the index?

The generated result is [`SCORECARD.md`](SCORECARD.md). This file is the map.

## What is graded

Two layers, deliberately separate:

- **Layer 1 (deterministic, all 98 letters)** — `extract.py` copies three
  regex-able signals out of each letter, never inferring a number that is not
  in the text: the opener's "S&P closed up/down X%" recap line, every SPY
  price named in the SPY sections (classed hold / break / target / mention by
  sentence keywords), and one record per "TICKER – Daily Chart" paragraph in
  Swing Stock Scans with its trigger price where one parses ("over 311",
  "over Friday's high"). `grade.py` grades them against Yahoo daily bars.
- **Layer 2 (interpretive, 31 letters 2025-12-29 → 2026-08-31)** — Claude
  read each letter's market-analysis sections and wrote `extractions/L2_*.json`:
  the lean (direction, conviction, hedged or not, with the sentence that
  carries it) and every conditional statement classed into a closed rule
  vocabulary (`grade2.py` docstring). Every level is checked to appear
  verbatim in the letter. Grading is then mechanical.

Windows are pre-registered from the letter's send time (converted to Eastern):
the recap week is the Mon–Fri ending on the last Friday before the send; the
forward week is the following Mon–Fri, only days after the send (a Monday
evening letter grades Tue–Fri). Swing ideas must trigger inside the forward
week; outcomes are 5 and 10 trading days after the trigger with MFE/MAE, and
every idea also gets a "bought at the first open" baseline and SPY over the
same window. Lean is graded on SPY Friday-to-Friday.

## Headline (as of 2026-09-05)

- **His scorekeeping is honest.** 39 recap lines parsed: 37/38 direction
  correct, 35/39 within 0.15 pp of the true move. He usually means Monday
  open → Friday close on SPY even when he writes "last week".
- **The directional lean has no edge over "up".** 25 directional leans in
  the Layer 2 window, 15 correct (60%); the forward week was up 19/31 (61%).
  Bullish leans 12/18, bearish 3/7. 23 of 31 leans were hedged with an
  explicit alternative path.
- **Levels are real, consequences are not.** "Must hold" levels held into
  Friday 34/44 times (77%) and 17/26 of the ones actually tested. But the
  bearish sequences ("acceptance below X then break of Y → lower") followed
  through in only 2 of the 7 cases where the break happened. Layer 1 agrees:
  break levels were reached 53% of the time, and SPY closed the week below
  them in only 38% of those.
- **Swing scans track the index with more noise.** 490 ideas, 188 triggered
  inside their week. 10-day return after trigger: mean +0.65%, median +0.54%,
  52% winners; SPY over the same windows +0.90% with 61% winners. Buying every
  idea at Monday's open: +0.75% vs SPY +0.77%. Typical best excursion +7.8%,
  worst −7.3%, so exits decide the P&L, not the pick. By year: 2024 beat SPY
  (+2.75% vs +1.01%), 2025 lagged (+0.80% vs +1.35%), 2026 lost (−1.29% vs
  0.00%).
- **The one macro scenario table graded so far was right**: the 2026-08-30
  letter's "HOT NFP → yields up, market down" fired on 2026-09-04 (payrolls
  162k vs 53k; 10-yr up; SPY down open-to-close and close-to-close).

Read: the letter is an accurate, well-structured map of where the levels are
and what he will do at them, with honest self-scoring. It is not a forecast
with measurable edge, and its bear warnings rarely play out within a week.

## Caveats

- Daily bars are Yahoo via yfinance; Yahoo's ^GSPC open is not a real print
  (SPY is used for opens), and split-adjusted histories can make an old
  trigger look absurd — `grade.py` rejects triggers more than 30% from the
  week's first open as `trigger_implausible` (9 cases).
- Regex coverage is partial: about half the swing ideas have no parsable
  trigger (pullback-style setups) and only get the Monday-open baseline; the
  2024 letters have no SPY section headings, so their level counts are thin.
- Layer 2 is one reader's classification. The quote next to every call is
  there so a second reader can disagree with the class, not the arithmetic.
- 31 weeks is a small sample for lean accuracy; the swing-idea sample (188
  triggered) is the statistically useful one.

## Refreshing (weekly, after the Sunday letter lands)

1. In a Claude Code session with the Gmail connector: search
   `from:newsletter@tradebrigade.co newer_than:8d`, then `get_thread` with
   `messageFormat: FULL_CONTENT`. The result exceeds the connector's inline
   cap and is written to the session's `tool-results/` directory instead of
   the context — that file is the ingest source. Append the date and
   threadId to `threads.txt`.
2. Run, from `yt-analyst/`:
   ```
   .venv/bin/python newsletters/tradebrigade/ingest.py     # tool-results → letters/
   .venv/bin/python newsletters/tradebrigade/extract.py    # letters → extractions/L1_*.json
   .venv/bin/python newsletters/tradebrigade/prices.py     # refresh data/prices.csv (merges)
   .venv/bin/python newsletters/tradebrigade/grade.py      # writes SCORECARD.md §1–4
   .venv/bin/python newsletters/tradebrigade/grade2.py     # appends §5 from extractions/L2_*.json
   ```
3. Write `extractions/L2_<date>.json` for the new letter by reading its SPY /
   QQQ sections (`sed -n '/Broad Market Analysis/,/Economic & Earnings
   Calendar/p' letters/<date>_*.txt`), then re-run `grade2.py`. Each call
   needs a verbatim quote and one of the rules in the `grade2.py` docstring.
4. Commit `extractions/` and `SCORECARD.md`. `letters/` and `data/` are
   working data and gitignored.

Grades for a letter are final only after its forward week closes, so the
scorecard is always one week behind the newest letter.
