# Video: 8O_GIxjhLkc

- **URL:** https://www.youtube.com/watch?v=8O_GIxjhLkc
- **First analyzed:** 2026-09-07
- **Title:** Textbook ES Short Using Smart Money & Order Flow
- **Channel:** Trader Dale — presenter introduces himself as "Dan from Funded Trader Academy" (spoken 00:03, two runs; unverified)
- **Uploaded:** 2026-08-19
- **Duration:** 11:44 (704 s)
- **Views:** 3,843
- **Bead:** dr-87x
- **Status:** closed

## Findings
**What it is.** A replayed, paper-traded ES short on TradingView **Bar Replay**, not a live trade. The opening slide says so: *"All trades presented are NOT TRADED IN A LIVE ACCOUNT and should be considered hypothetical."* (00:01, `onscreen_text`, two runs agree word for word). The screen is a 1-minute chart left, 1-hour right, both `E-mini S&P 500 Futures (Sep 2026) · CME`, symbol `ESU2026`; the replay clock reads `Mon 17 Aug '26 10:41` at the setup and `10:51` at the exit. **Verified by frames** (`frames-000-020/f_0006.jpg`, `frames-900-935/f_0009.jpg`, `f_0016.jpg`).

**The trade, from the order labels and toasts (frames).** Sell 1 `ESU2026` at **7,795.50**; stop **7,800.00**, labelled **−225.00 USD**; target **7,790.00**, labelled **+275.00 USD** (toast *"Take Profit order placed on CME_MINI:ESU2026 — Buy 1 at 7,790.00"*, ≈09:16). The stop was later tightened to 7,798.50 and cancelled when the target filled (toast *"Stop Loss order cancelled … Buy 1 at 7,798.50"*, ≈09:30). Arithmetic closes at the ES multiplier: 4.5 pt × $50 = $225, 5.5 pt × $50 = $275. Realized **1.22R** on the executed fill. **Verified: frames + arithmetic.**

**"6.5-point base hit" (spoken 00:06) is the marked-up plan, not the fill.** The intro chart carries a hand-drawn *Short* arrow from ≈7,796.50 to an *Exit* label at 7,790.00, which is 6.5 points; the replay execution got 5.5. Small, but the headline number is the drawing.

**Method vocabulary.** Smart Money Concepts on the higher timeframes: 1h/4h "imbalance" (fair value gaps, drawn as boxes, `1h FVG` / `15m FVG` labels on screen), plus **BULL TRAP / BEAR TRAP** labels from an indicator titled `SMC HTF/LTF` (frames). Order flow is a bubble overlay he calls **"Delta Flow"** (spoken 00:23) with a per-bar Volume / Delta / Min delta / Max delta table under the 1-minute chart (frames). *"The dark ring around the bubble indicates higher than 50 contracts per second"* (spoken 07:44, unverified). Entry criteria, spoken 08:20: shift in control, seller absorption, exhaustion, and a 1-minute break of structure, at a retest of the **7,800 "psychological level"** (spoken 07:21).

**Pitches.** Free book download *"Order Flow Trading Secrets"* (banner 04:19), a VWAP book (10:34), Funded Trader Academy membership (spoken 11:30).

**Gemini reliability on this video — a corpus-level finding.** The wide pass and the first zoom **both** read the chart as `ESU2024`, August 2024, priced 5,580–5,650, and the wide pass logged the clash with the spoken "August 17th, 2026" as the *presenter's* error. The second zoom read 7,79x but assigned the ticket wrongly (entry 7,798.50, stop 7,801, target 7,795). Frames contradict all of it. The dollar labels were the tell: neither fabricated set closed against −225 / +275. See LESSONS.md 2026-09-07.

**Relevance to us.** It is ES, it is order flow, and the trade is coherent. But it is a sim replay of one setup, the structure is SMC (traps, FVGs) with a proprietary bubble indicator, the reward is 1.2R, and there is no statistic. As a specimen of the presenter's acuity it shows discipline (defined criteria, stop placed, target at the prior swing low) and nothing that could be tested.

## Sessions
- **2026-09-07** — Scouting pass for Steve's question about Trader Dale's acuity on SPX/ES [dr-87x]. Wide pass (64K tokens) + two zooms + two frame pulls. Verdict: hypothetical replay, not live; trade figures frame-verified and reconciled at $50/pt; Gemini's price-axis readings wrong in all three runs. Card closed. Runs: 170535 (wide), 170643, 170647 (zooms).

## Lessons (this video)
- TradingView, split 1m / 1h, Bar Replay with the paper-trading panel; ticket events arrive as toasts bottom-left, which are the most legible numbers on screen — zoom on them and pull frames.
- Trader Dale's channel carries Funded Trader Academy presenters; check who is speaking before attributing a view to Dale.
- Every video opens with the same ~20-second disclaimer card; clip windows can start at 00:20.
- Gemini cannot read this channel's ES price axis at YouTube-URL resolution (three runs, three wrong sets). Frame every number.

## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260907-170535 [full] gemini-flash-latest (tok 64493/1205) — Q: This is a worked ES (S&P 500 futures) short by Trader Dale. Report: (1) the inst… — runs/20260907-170535/
- 20260907-170643 [00:00-01:50] gemini-flash-latest (tok 10369/1171) — Q: Transcribe verbatim: (a) the full disclaimer text on screen at the start; (b) th… — runs/20260907-170643/
- 20260907-170647 [07:20-09:45] gemini-flash-latest (tok 13522/892) — Q: Transcribe verbatim every number spoken or shown for this trade: the level being… — runs/20260907-170647/
