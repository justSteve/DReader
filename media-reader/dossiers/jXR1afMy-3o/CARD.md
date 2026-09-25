# Video: jXR1afMy-3o

- **URL:** https://www.youtube.com/watch?v=jXR1afMy-3o
- **Title:** PbD: The World's BEST trading strategy (explained in detail)
- **Channel:** Tom Vorwald EN (@tom_vorwald_en) — "Trade The Traders" / WorldClassEdge
- **Uploaded:** 2026-01-23 · **Duration:** 12:08 · **Views:** 71,273
- **First analyzed:** 2026-09-06
- **Status:** closed
- **Bead:** dr-zk8 (Vorwald orderflow sweep)
- **Sweep:** see [playlist synthesis](../../playlists/vorwald-orderflow-sweep.md)

## Findings
_(curated by Claude Code: verified findings with timestamps)_

The fullest statement of the PbD framework, and **the video that supplies the
candle-close rule the rest of the channel only gestures at.**

**The 70/30 split.** P and b logic applies to roughly **30%** of market
conditions (01:29); the remaining **70%** is balance (01:39). This is the
channel's fifth independent statement of the same figure — see
[K8qtT2_axPo](../K8qtT2_axPo/CARD.md) 10:41,
[YmygDgtoxO8](../YmygDgtoxO8/CARD.md) 05:51,
[Ly62G168MkQ](../Ly62G168MkQ/CARD.md) 15:46 and
[43JaKHRvxHk](../43JaKHRvxHk/CARD.md) 02:18. **Internally consistent across
five videos**, which is worth something even though it is unsourced.

**Closing prices are the rule here, stated three times:**
- *(Quote marks removed 2026-09-06 — the string below was Gemini's paraphrase,
  `kind: spoken`, `verbatim: null`. What he says at 05:03–05:16 is an
  observation, not yet a rule: "always there, where the market moves out of
  balance, that is above the value area and below the value area, I very often
  see candlesticks with closing prices and opening prices." The **rule** form
  arrives at 05:36 — "I use closing prices to locate where the so-called
  break-off edges are" — and at 08:56, "the rules for counting closing prices".
  The card's substance stands; the attribution did not.)*
- looking for candle closes outside the Value Area to confirm moves out of
  balance"* (05:15)
- he uses **closing prices** to identify break-off edges in the volume profile
  (05:40)
- **candle-close counting rules** determine whether trend continuation holds
  (08:57)

**This corrects a gap recorded on [HySZZSjMxF8](../HySZZSjMxF8/CARD.md)**, where
the description promised a closing-price rule and the video delivered only an
aside. The rule exists — it lives in the PbD videos, and it aligns the channel
with SMDX's `"CLOSE BELOW MOST RECENT HL"` rather than leaving it unspecified.

**The entry moment**, German on screen (00:19):
> `Ein Ausbruch aus einer P-Formation gibt dir den entscheidenden Moment an,
> wann du traden solltest.`
> — "A breakout from a P-formation tells you the decisive moment when you
> should trade."

Four breakout/rejection scenarios from a P-formation are diagrammed at 09:05.

**Named concepts:**
- **"Break-in"** (10:04) — **treat this term with caution.** The crisp
  definition below is Gemini's (`verbatim: null`); what he actually says at
  09:47–10:02 attaches the word to a different sentence: *"the market drops
  down and gives me a P. And now I have the opportunity to recognize that
  buying is happening again… We call this a break-in."* The two readings are
  compatible, but note the audio is an **AI dub of German**, and German
  *Einbruch* — a plunge or collapse — would also surface as "break-in". The
  corpus should not build vocabulary on this until frames at 09:45–10:20
  settle whether it is a term or a translation artefact. As glossed: a move
  extending beyond the range and then returning
  inside. The corpus had no name for this; it is the failed-breakout case.
- **D-setup** (11:10): the balanced profile shaped like a D.
- **Single prints = aggressive forced buying** (05:58).
- **Low-volume nodes** = price zones where the market slips into imbalance (02:52).
- **Market Profile** = how much **time** the market spent at price levels (02:35);
  **Value Area** = where the market finds **acceptance** (04:42).

**On the box simplification**, on screen at 06:49:
> *"The Volume Profile and the corresponding box are always closely related…
> the box is a simplification of the Volume Profile and at the same time a
> simple orientation aid. The boxes help us organize market movements within an
> overarching structure."*

Platform **probably ATAS** showing **probably FDAX** with TPO and volume profile overlaid (02:03) — the run's own uncertainties field says the ticker header and exchange are *"partially obscured and low-resolution"*, and the transcript names neither. Stated flatly on this card until 2026-09-06.
German label diagram at 04:28 matching the one in
[YmygDgtoxO8](../YmygDgtoxO8/CARD.md), plus `daily high / closing price /
opening price`.

**No live trade, no stop/target distances, no R:R, no win rate.**

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

- **2026-09-06 — comparative wide pass (epic dr-zk8).** Standardised
  orderflow wide pass, identical question across all 19 sweep videos. Verdict: the framework's fullest statement. Supplies the candle-close rule three times, correcting the gap logged on HySZZSjMxF8, and names the 'break-in' (failed breakout).

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

- **This is the card to cite for the channel's close-vs-wick rule.** Closes
  confirm; wicks do not. Stated three times (05:15, 05:40, 08:57).
- "Break-in" — **provisional**; may be an AI-dub rendering of German *Einbruch* (a plunge). Not yet safe as corpus vocabulary. As glossed, extend beyond the range then return inside — a name the
  corpus lacked.
- The 70/30 balance/imbalance split is now attested in five separate videos.


## Run log
_(machine-appended by yta.py — do not edit above this line's entries)_
- 20260906-101517 [full] gemini-flash-latest (tok 66996/1573) — Q: Map this video for an analyst building a comparative corpus on ORDER FLOW and vo… — runs/20260906-101517/
