# Scope edits log

Steve's rule (2026-09-07): **everything in the reader relates to SPX/ES.** No
details on other instruments. If a passage is pertinent to general order-flow
theory but is worked on another instrument (the Euwax Sentiment digression, a
DAX ladder, a gold profile), it is edited out of the human-facing `READ.md`.
Cuts inside a quotation are marked `[...]`, the read's existing convention for
elision. `CARD.md` is the agent-facing record and is **not** edited for scope;
the reader shows it collapsed and labelled unedited.

Each entry: what was cut, from where, and why. Corrections of fact live in
`AUDIT.md`; this file is scope only.

## 2026-09-07 · `yWO8hVpRXeY` — the live DAX trade

Omitted from the reader entirely (`build_reader.py` `EXCLUDE`). The whole video
is a DAX session, Euwax Sentiment included. Card and read remain on disk.

## 2026-09-07 · `vl01TiVTuoQ` — Vorwald, order-flow guide

- L0, L1 ¶2, L2 "The method is calibration": the market-by-market size table
  (DAX 1, 1, 2, 4, 3, 5, 33; crude; bonds 5–6k a side; gold 2/4/6) reduced to
  the S&P figures: the 325 ask here, the 676 bid in the companion video, the
  250–300 threshold from the heatmap video.
- L3 "The living book" 03:39: the DAX ladder elided from the quote; the
  crude-oil quote removed; the aside's two caveats about crude and DAX
  figures removed with them.
- L3 "The scalper's desk" 09:01: passage removed (many-market desk tour, gold
  and Bund sizes, advice to learn the book on ZN / Euro Stoxx / 6E / 6B).
- Kept: 03:10 "DAX future has completely different prices … than S&P 500" —
  one clause making the know-your-product point, no figures.

## 2026-09-07 · `usho6UVLqkE` — Vorwald, DOM & footprint

- L0 "market by market" dropped. L1 and L2 calibration paragraphs reduced to
  the ES blocks of 74 and 48; the Russell 2247.1 level and the DAX ladder cut.
- L3 02:31 retitled "What one market order does"; the Russell setup elided,
  the sweep mechanics kept.
- L3 03:43 retitled "Blocks on the ES"; the DAX ladder elided from the quote;
  the aside no longer tabulates DAX and bond sizes and no longer notes the
  repeated "four contracts".
- L3 04:45: the 2,246.4 price elided (`[one] price range`); the aside's
  Russell attribution replaced by a note that the book is not the ES.

## 2026-09-07 · `RwQBdF9TSvc` — Vorwald, the ICT-rejection podcast

- L1 and L2: DAX 20-point spreads and Euro Stoxx 300–500 → single digits
  removed; the "sometimes 80% of the book missing" figure kept.
- L3 26:10: the DAX, Euro Stoxx and negative-oil remarks elided; the aside's
  hedge list reduced to "sometimes 80%".

## 2026-09-07 · `m3IMdc7QwN4` — Vorwald, the PbD key

- L2: "Gold sells off" → "Price sells off".
- L3 02:26 retitled "The b"; "the gold chart" and "the price of gold" elided;
  the aside says the chart is not the ES.

## 2026-09-07 · `Vd83oo_geMk` — Vorwald, heatmap & liquidity

- L3 04:13 "The book array": the instrument roll-call (ZM, CL, Russell,
  Nasdaq, S&P, FDAX) elided; the 20-rows point kept.

## Not yet scoped

The three playlist syntheses in `playlists/` and the 25 card-only videos still
carry other-instrument detail; they are shown as written.
