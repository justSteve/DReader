# Playlist synthesis — Carmine Rosato, "Trading Orderflow Series" (8 episodes)

- **Playlist:** https://www.youtube.com/playlist?list=PLWQioWs8oOiFKQnwIIYbw8N7ks7d-UAPQ
- **Analyzed:** 2026-08-28 · bead epic `dr-08s` · cards in `videos/<id>/CARD.md`
- **Scope:** playlist items 2–9 (ep. 1–8). Item 1 (`sPqeW4j-8Zk`, intro) skipped per Steve.
- **Method per video:** wide pass → zooms on load-bearing numbers → arithmetic → frames → Opus verifier (eps. 1–7) or direct cross-reference (ep. 8).

| # | Ep | Video | Uploaded | Len | Card | Verified how |
|---|----|-------|----------|-----|------|--------------|
| 2 | 1 | QaNPAaEnB5E — auction theory | 2024-10-14 | 21:47 | closed | 31 frames + Opus |
| 3 | 2 | eJZhX6Xz4cU — footprint & delta | 2024-10-18 | 24:53 | closed | 67 frames + Opus |
| 4 | 3 | tgQC7Dpcc8A — DOM & Bookmap, 4 trades | 2024-10-24 | 28:28 | closed | 96 frames + Opus |
| 5 | 4 | 0QlGCz6U_1g — retail vs institution | 2024-10-29 | 16:25 | closed | 46 frames + Opus |
| 6 | 5 | 5qBo04SMUFc — S/R validation, 1 trade | 2024-11-08 | 29:21 | closed | 73 frames + Opus |
| 7 | 6 | w7tvJCuZAq8 — volume frameworks | 2024-11-13 | 31:28 | closed | 76 frames + Opus |
| 8 | 7 | 7facFfjQ0UE — CLC rule, execution, 2 trades | 2024-11-18 | 32:19 | closed | 78 frames + Opus |
| 9 | 8 | 00QtD-RosLg — recap | 2024-11-25 | 26:24 | closed | 20 frames, direct |

## The method, assembled across episodes

**Premise (ep. 1, 4).** The market is an auction. Price moves only because
aggressive (market) orders consume passive (limit) liquidity; indicators
and "concepts" are downstream of order flow. Balance = a range where buyers
and sellers agree (fair value); an event creates imbalance → new range.
Retail buys breakouts/dips and sells panics; institutions do the opposite —
buy at *wholesale* (demand, stop hunts) and sell at *market price* (supply,
breakouts). Retail is the liquidity ("bait fish").

**Instruments (ep. 2, 3).** Time & Sales (who is the aggressor); footprint
charts (per-price bid×ask, delta = ask − bid, total volume; his layout on
Sierra Chart: ES, 20-tick/5-point RANGE bars, columns = total volume /
delta / delta-colored profile); DOM (VPS | VPB | Bid | RB | RA | Ask |
Price | VPD | SVP; VPD = VPB − VPS, SVP = VPS + VPB — pixel-proven);
Bookmap heatmap (bands = resting liquidity, bubbles = executed aggression;
green = buys hitting the ask, red = sells hitting the bid). Charts are
ThinkorSwim captures with his custom study `BuyingVsSelling_Carmine (…)`.

**Signals (ep. 2, 5, 6).**
- *Trapped participants / absorption*: lots of aggressive volume at a
  price with NO follow-through ⇒ a passive counter-party is active ⇒
  reversal candidate. Heavy selling that doesn't drop price = passive
  buyer; heavy buying that doesn't lift = passive seller.
- *Volume tail*: prints thin out at an extreme (e.g. 29/29, 136/136, 51/51
  at the top of the bar) — the last buyer bought; level validated.
- *Delta outliers*: no threshold — "just an OUTLIER in the data" (ep. 3);
  examples −735/−1171 at the Oct 3 low, +1633 at the Sep 27 break, +4000
  at the Oct 9 level, −750/−538 at a flipped level (ep. 6).
- *Good vs weak S/R (ep. 5)*: a level is good when validated by order flow
  (exhaustion/absorption); weak when its bounce came from aggressive
  buyers rather than seller exhaustion.

**Frameworks.**
- *Reversal-first at breakouts (ep. 6)*: ~99 % of the time look for the
  reversal on the first test; aggressive volume into a level with no
  continuation = fade it.
- *Breakout continuation (ep. 3, 6)*: Step 1 confirm strong volume in the
  trade direction; Step 2 pullbacks HOLD (no rejection). Never buy the
  initial break — let it break, buy the pullback / short the pop; a
  defended retest proves the participants are "even more powerful".
- *How I play S/R (ep. 5)*: (1) break → retest; (2) reversals off trapped
  participants — "where there is PAIN there is GAIN"; (3) get in BEFORE
  the level breaks, with confirmation, using the level as target.
- *CLC rule (ep. 7)*: CONTEXT (trend; today's volume vs average; the
  timeframe table 1D:1m … 3Y:W is for context and location only) →
  LOCATION (a level of interest: supply/demand, S/R) → CONFIRMATION (are
  buyers buying or trapped? sellers selling or trapped?) read in "The
  Now" — live tape/footprint, never a candle close. Waiting for a candle
  close moves the stop from ~2 pts to ~7 pts and kills the R (ep. 7).

**Execution and risk (ep. 3, 5, 7), from the journaled trades:**

| Date | Dir | Contracts | Entry (derived) | Stop | Risk | Target | Planned R | Result | Realized R | Ep |
|------|-----|-----------|-----------------|------|------|--------|-----------|--------|------------|----|
| 2024-09-26 | short | 30 | 5813.0 | 5815.0 (2 pt) | $3,000 | 5800.0 | 6.50R | +13.5 pt $20,250 | 6.75R | 3 |
| 2024-09-27 | long | 30 | 5810.25 | 5808.5 (1.75) | $2,625 | 5820.0 | 5.57R | +10.25 pt $15,375 | 5.86R | 3 |
| 2024-10-02 | long | 30 | 5742.5 | 5741.0 (1.5) | $2,250 | 5755.0 | 8.33R | +11.0 pt $16,500 | 7.33R | 3, 4 |
| 2024-10-03 | long | 30 | 5740.5 | 5739.0 (1.5) | $2,250 | 5753.0 | 8.33R | +14.5 pt $21,750 | 9.67R | 2, 7, 8 |
| 2024-10-09 | long | 30 | 5800.5 | 5797.0 (3.5) | $5,250 | 5812.0 | 3.29R | +14.5 pt $21,750 | 4.14R | 3 |
| (undated) | short | 25 | 5643.0 | 5646.0 (3) | $3,750 | 5631.0 | 4.00R | +17.5 pt $21,875 | 5.83R | 5 |
| 2024-11-11 | short | 40 | 6044.5 | 6046.0 (1.5) | $3,000 | 6037.0 | 5.00R | +11.5 pt $23,000 | 7.67R | 7 |

Every figure is on screen and closes arithmetically (P&L = pts × contracts
× $50; planned R = target/risk; realized R = P&L/risk); entries are
derived from stop + risk (never displayed). Pattern: stops of 1.5–3.5 ES
points placed just beyond the absorption level, targets of 7.5–13 points
at the opposing level, planned 3–8R, realized 4–10R. Seven winners are
shown; no losers are shown — the sample is curated, not a track record.
The "$208,000 in September" and "236 profitable days" (Goldman) overlays
are unverified marketing claims.

**What is NOT specified anywhere in the series:** a numeric delta or
volume threshold; position-sizing rules beyond "30 contracts"; exit rules
beyond "target at the opposing level, trail after"; any win rate.

## Cross-episode consistency (free verification)
- The Oct 3 2024 trade appears in eps. 2, 7 and 8 with identical fields;
  ep. 7's Bookmap tooltip (Δ −1171, vol 1739 at 5739.75/5740, 09:54)
  matches ep. 2's footprint outlier at 5740.00.
- The Oct 2 2024 session backs ep. 3's trade 4 and ep. 4's stop-hunt
  example (`RESISTANCE ($5730)`).
- The ES 1-min chart with `15m ($5771)` / `RESISTANCE ($5730)` is the
  stock backdrop of eps. 1, 4, 8.
- Slides recur verbatim (auction summary, Trapped Traders, Retail vs
  Institutions, How Does Retail Trade?, bait fish).

## Where Gemini failed, and what caught it (see LESSONS.md)
Slides and text overlays: essentially perfect (dozens of word-for-word
matches). Failures cluster in chart-level text and dense numbers:
`$5`→`60` and `$`→`1` glyph confusions on price labels; 20–25 % per-row
error on ladders > 10 rows; adjacent-row bleed; wrong-tab instrument;
millisecond→PM timestamps; derived figures reported as on-screen; spoken
round-offs reported as values; prior-knowledge brand names; skipped
segments; slide timestamps 2–4 s early. Caught by: arithmetic closure
(trade logs, histograms), parity (delta ≡ volume mod 2), price-axis sanity
(0.25 multiples; ES vs NQ level), wide-vs-zoom disagreement, and frames.
