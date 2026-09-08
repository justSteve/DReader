# Transcript audit log

Composing the human-facing `READ.md` layer (epic `dr-aib`) turned out to audit
the machine-facing cards. Each composer checks every figure, name and quoted
string in `CARD.md` against the transcript and the underlying Gemini run JSON,
reports, and never edits the card. Corrections are reconciled here and applied
centrally, because a hardened figure usually appears in more than one file.

**Failure classes** (see `.claude/skills/composing-card-reads/SKILL.md`):

1. A hedge hardened into an assertion
2. A paraphrase tabulated as a quote (`verbatim: null` in the run JSON)
3. A spoken claim attributed to the screen (`kind: spoken`)
4. A number the transcript contradicts, or that appears nowhere in it
5. A name or term the card gets wrong

---

## 2026-09-06 · `NkQeOVDTAec` — Vorwald, volume profile · **class 1, 2**

Found independently by both bake-off composers.

| | |
|---|---|
| He said | *"my average risk-reward ratio is **maybe a two**"* |
| Gemini claimed (`kind: spoken`, `verbatim: null`) | "Target average risk-reward ratio is greater than 2" |
| Card tabulated | `greater than 2`, under a column headed **"Stated value"** |
| Sweep synthesis repeated | `> 2`, with expectancy arithmetic built on it |

The 50% hit rate was likewise conditional — *"if you should now… reach a hit
rate of 50%"* — and was recorded as a "planning hit rate". Only the **200–300
trades** figure is flatly stated.

**Fixed** in `videos/NkQeOVDTAec/CARD.md` (Findings table, Sessions verdict,
Lessons bullet), `videos/uFxYcpiaOpw/CARD.md` (its comparison against this
card) and `playlists/vorwald-orderflow-sweep.md` (numbers table and the
arithmetic paragraph). Repo-wide sweep for the hardened phrasing is clean.

**Note the cascade:** I first fixed only the Findings table and reported it
done. Three other copies were still standing. That is why corrections
reconcile centrally.

---

## 2026-09-06 · `QaNPAaEnB5E` — Carmine ep. 1, auction theory · **class 2, 4, 5**

**1. Class 4 — the headline marketing figure is contradicted by his own audio.**
The card and the playlist synthesis both carry an on-screen overlay reading
`SEPTEMBER $208,000`. At **00:02–00:07** he says: *"last month was my most
profitable month, I came out with a gross profit of **$28,000**."* A 7.4×
difference. The card's figure came from a `verbatim` on-screen capture, so it
is not obviously the wrong one — but neither is frame-verified (no frames exist
at 00:00–00:10), and captions mis-hear digits elsewhere in this same
transcript. **Both card and synthesis now record the contradiction and neither
figure should be repeated until frames settle it.**

**2. Class 2 — quotation marks around a paraphrase.** The card rendered the
19:15 funnel diagram as everything feeding into *"actual buy/sell orders
executed"*. That claim is `kind: visual`, **`verbatim: null`** — Gemini's
words, not the screen's, and no frames were pulled at 19:15. His actual line at
19:44 is *"regardless of the strategy, regardless of the tool, an order has to
be placed."* **Fixed** — quotation marks removed, transcript line quoted instead.

**3. Class 4 — a term that appears nowhere.** The card listed the dismissed
indicators as "(MAs, RSI, **MACD**, ICT/SMC)". MACD is never spoken; he names
moving averages, RSI, Fibonacci, ICT and Smart Money Concepts. MACD's only
source is a `verbatim: null` visual claim with no frames. **Fixed** — flagged
as unattributable without frames.

**4. Class 5 — bids recorded as asks.** The real-estate ladder was carded as
"$100k/$200k/$300k/$400k **asks**". Transcript 08:42–09:01: the ask is
$400,000, and *"you're willing to pay a hundred, you're willing to pay 200, but
now you put out a **bid** for $300,000."* Three of the four are bids, and the
run JSON itself said "asking prices and buyer bids" before the card compressed
it. **Fixed.**

**Clean in this card:** the New Car diagram figures, every order-mechanics
slide line against the spoken 12:17–15:12, the 14:36 summary word-for-word, the
chart narration, and the Gemini-error list. No hedge was hardened anywhere.

---

## 2026-09-06 · `tgQC7Dpcc8A` — Carmine ep. 3, DOM & Bookmap · **class 1, 2**

Trade dashboards, DOM ink and slide strings all check out. Two findings, plus
one addition that changes a corpus-level claim.

**1. Class 1 — a hedge compressed into a binary.** The card read "a tail INTO a
breakout on strong volume is discovery, **not exhaustion**". His framing is a
question the auction has not yet answered (12:57–13:16), and in this instance
it resolved as *rejection* (14:12–14:32). **Fixed** — hedge and outcome restored.

**2. Class 2 — the card's own abridgement inside quotation marks.** Three
on-screen lines at 23:30 were condensed into one and left quoted. The full
`verbatim` exists in the run JSON. **Fixed** — restored verbatim.

**3. ADDITION — the series does supply a delta calibration method.** The
synthesis said the series states "no numeric delta or volume threshold". Too
strong. At 09:02 he disclaims a fixed threshold — *"I don't look for specific
numbers, I look more so for outliers in the data"* — and then demonstrates one:
*"we could see an average there — like 500 is the high side and the low side is
like a 300 delta or 200 delta. If I saw a delta for like over a thousand here
then there would be an outlier."* A session-and-instrument baseline, not a
constant. **Added to the card; the synthesis line refined.** It narrows without
closing the gap the Vorwald channel fills, whose threshold is a different
quantity — resting order *size* (ES > 250–300 contracts), not delta.

---

## 2026-09-06 · `0QlGCz6U_1g` — Carmine ep. 4, retail vs institution · **class 2**

**1. Class 2 — a quoted slide string matching neither screen nor speech.** Card:
*"how many times have you stopped out … and then the market moves in your
favor?"*. Screen: *"…for a loss AND after the market eventually moves in your
favor?"*. Spoken: *"…for a loss and then the market eventually moves…"*. **Fixed.**

**2. Class 2 — a dropped word.** Card: *"Would you buy at this green box?"*.
Screen: *"Would you buy **the stock** at this green box?"*. **Fixed.**

**3. Bookkeeping.** The Sessions entry cited three zoom runs (`-113811`,
`-113856`, `-113926`) that do not exist. Real IDs: `-113702`, `-113715`,
`-113728`. **Fixed.**

**AND A CORRECTION TO MY OWN CORRECTION.** The ep. 1 entry above led me to
write, in the playlist synthesis, that the Goldman *"236 profitable days"*
overlay was "not frame-verified — do not repeat until frames settle it". **That
is wrong.** `videos/0QlGCz6U_1g/frames-233-243/f_0003.jpg` carries every figure
(236 / 15 / 41 / 112 / $100M / $50–100M / $18.1B / 53% / 2012) and the histogram
bars close arithmetically against them. It is cited evidence about Goldman's
2012 record, not a claim about the presenter, and it is unrelated to the
$208,000 overlay. **Synthesis fixed.** Caught by the ep. 4 composer.

---

## 2026-09-06 · `eJZhX6Xz4cU` — Carmine ep. 2, footprint & delta · **class 1, 2, 5**

Every number holds — the delta examples, the journal figures, the ladder print.
Where captions disagree the card correctly carries the screen value.

1. **Class 2** — Setup 2 was carded as "enter short **against the high**". That
   phrasing is Gemini's run summary, never Carmine's. **Fixed**, his words quoted.
2. **Class 1** — "Strong selling but market not moving lower ⇒ a passive buyer
   is active" drops two hedges: the slide says *"it's a **sign**"*, the audio
   *"**maybe** somebody's buying… a **good chance** a buyer is active"*. **Fixed.**
3. **Class 5** — the header credited "Carmine Rosato **(Jumpstart Trading)**".
   That brand appears nowhere in the transcript or in any of the five run JSONs,
   and ep. 5's card explicitly records no wordmark on screen. **Removed** — it
   may well be right, but its provenance is not in this dossier.
4. **Bookkeeping** — run IDs `-110709`/`-110838` do not exist; real are
   `-110717`/`-110823`. **Fixed.**

---

## 2026-09-06 · `00QtD-RosLg` — Carmine ep. 8, recap · **clean**

No hedge hardened, no paraphrase quoted, no spoken claim attributed to screen,
no name wrong. One loose gloss fixed: the retail behaviours were listed as
"longing trendlines" where his only trendline example is a **short** (05:56).

---

## 2026-09-06 · `ZVvVgcX84F0` — tastylive, wide butterfly · **class 1, 2, 4**

The frames-verified figures all hold. Three inferences had been tabulated as
facts:

1. **Class 4 — "Position already held (BTO/STO tags on the chain)".** On
   tastytrade those badges mark legs *staged* in the New Trade panel; the frame
   shows **Review & Send un-pressed** and a stale limit, and he says only *"what
   I have loaded up here"* and *"You don't even have to route them as orders"*.
   Whether the position was live is not established. **Corrected to "staged".**
2. **Class 2 — "sell the two 7660/7665/7670 flies".** No strikes are spoken:
   *"if it drops down to 7665, then **maybe** I'll sell these two put butterflies
   that I have embedded here."* The strikes came from a `verbatim: null` claim,
   and they contradict the card's own count, which lists **one** such fly.
   **Strikes withdrawn, hedge restored.**
3. **Class 2/4 — "7645/7650/7655 ≈ $0.65".** Strike triple never spoken (*"the
   60 strike or the 50 strike… I dragged the wrong thing"*), and on the 05:59
   chain a fly centred at 7655 is ~0.30. **Strikes withdrawn; the $0.65 stands
   as spoken and unverified.**

**ADDITION — the decomposition balances in price, not just in contracts.** From
the 05:59 chain frame, the five embedded flies' mids (0.825 / 0.95 / 0.80 /
0.55 / 0.30) weighted 1·2·3·2·1 sum to **6.525** — the wide fly's own mid, the
spoken "$6.50". The 07:06 frame balances again at 6.775 both ways. Because the
decomposition is an identity in contracts it must hold in prices all day, and
this is the cleanest confirmation of the video's whole thesis. **Added to the card.**

---

## 2026-09-06 · `w7tvJCuZAq8` — Carmine ep. 6, volume frameworks · **class 2, 5**

**The interesting one is a mis-attributed error.** The card filed "−583 (actual
−538)" under *Gemini errors caught*, and Lessons called it a transposition
caught by parity. But at 27:21 **the presenter himself says** *"a negative
Delta of −750, −5, uh, 83"* — Gemini reported the audio faithfully. The pixel
value −538 stands. **The transposition was his, not the model's.** Fixed; this
matters because the card was using it as evidence of a Gemini failure mode.

Also: Example 3's quoted string is a `verbatim: null` paraphrase lightly
re-edited; two slide quotes were smoothed while marked verified ("is" → "are",
a dropped *"this just shows"*); and a 30:09 sentence about stop placement is
Gemini's paraphrase, though the card does label it "Spoken". The ~99% hedge is
correctly preserved. A fourth continuation example (22:47–23:25, −462 / −514)
is absent from the card and now appears in the read, flagged unverified.

---

## 2026-09-06 · `5qBo04SMUFc` — Carmine ep. 5, S/R validation · **class 2, 4, 5**

**1. Class 4 — the card contradicts him.** It said the double-top linkage was
*"inferred… not stated"*. At 25:38–25:51 he states it: *"this is how I could
look to capitalize on this setup… capitalizing on this failed breakout above
the resistance level"*, with $22,000 on $3,700 risk. **Fixed** — and the
underlying caution survives on better ground: the derived entry 5643 sits ~25
points below the 5668.50 double top, so the journaled trade was not a short at
the top.

**2. Class 5 — a name the card wrongly dismissed.** The header called Gemini's
*"InvestiTrade"* unsupported and the Lessons list called it invented. At 17:25
he says *"I talk about this a lot in the invested trade Community"*. Ep. 7
confirms it independently at 26:37: *"anybody in the invest trade Community"*.
**Heard, not invented. Fixed on both cards.**

**3. Class 2** — *"over +1200"* in quotes; he says *"a plus 1200 delta"*. The
"over" was Gemini's. **Fixed.** Two slide quotes are also abbreviated inside
quotation marks (meaning intact, wording not verbatim).

**Gap:** at 13:47 he says *"this is a 30 minute footprint here"*; the card
describes the chart only as range bars. Unresolved, flagged in the read.

---

## 2026-09-06 · `7facFfjQ0UE` — Carmine ep. 7, CLC & execution · **class 1, 2, 4, 5**

**1. Class 4 — a wrong ratio, contradicted by his words and by the card's own
arithmetic.** The card put the order-flow entry against the late entry at
*"~1:1 vs ~4:1"*. He says *"I'm risking two points to make 12 points… now I can
get a **6 to 1 or better**"* (21:12–21:31), and the card's own figures give
**6.25:1** for the order-flow entry and **1.8:1** for the 7-point late entry.
Both stated ratios were wrong. **Fixed.**

**2. Class 4/5** — the card had him saying *"1-point"* risk. He says *"about a
1.5 point risk"*, *"1.5, even at most a two-point"*, *"a one, two-point stop
loss"*. The bare "1-point" was Gemini's summary wording. **Fixed.**

**3. Class 5** — *"Invest Trade"* dismissed as unsupported; he says it at 26:37.
**Fixed** (see ep. 5 above).

**4. Class 1/2, minor** — *"delta runs −254 → −1100"* at a precise 9:52:54; he
says *"as it broke the low at 952 **50-ish**… **over** 900 more aggressive
contracts"*. Hedge hardened, "over" trimmed. And *"without looking back"* in
quotes is Gemini's paraphrase of *"the market never looked back"*.

**5. Provenance unlabelled, low severity** — four figures (demand-zone top
5743.75, prior-bar vol 951, resting-bid band 5740.25–5741.25, Sierra clock
9:52:08) appear in neither transcript nor run JSON. Probably pixel reads, but
the card does not say so. Flagged for labelling, not correction.

**Clean:** the Bookmap tooltip (09:54 · 5739.75/5740.00 · vol 1739 · delta
−1171) has a non-null on-screen verbatim and matches ep. 2 independently; both
TradeZella panels; the timeframe table; the 1–2 pt stop.

---

## Branding, reconciled across the Carmine series

Three cards carried three different brand claims. Settled:

- **"Jumpstart Trading"** (eps. 1, 2 headers) appears in **no transcript and no
  run JSON** anywhere in the series. **Removed from both** — it may be correct
  from outside knowledge, but its provenance is not in this dossier.
- **"InvestiTrade" / "Invest Trade"** was dismissed on eps. 5 and 7 as a Gemini
  invention. He **says it aloud in both**: *"the invested trade Community"*
  (ep. 5, 17:25) and *"anybody in the invest trade Community"* (ep. 7, 26:37).
  **Restored on both** as spoken, not on screen.

---

## Operational note for parallel composition

An ep. 5 composer reported its scratch helper file being **overwritten by a
sibling agent** mid-task; it recovered by switching to video-specific
filenames. Later dispatches now instruct composers to namespace scratch files
by video id. Worth carrying into any future fan-out.

---

## 2026-09-06 · `Vd83oo_geMk` — Vorwald, heatmap & liquidity · **class 1, 2, 3, 4**

**This audit overturned the corpus's headline cross-source finding, which was
mine and which was overstated.**

**1. Class 1 — "rejects heatmaps" was never his position.** The card and the
sweep both said institutions and his own group *"do not rely on heatmaps"*, and
the sweep called this the sharpest conflict in the corpus. The transcript:

- *"the heat map is such a wonderful tool that's being heavily promoted these days"*
- he **demonstrates it on screen**: *"here we can take a look at what the heat map
  is currently showing us for the SNP500"*; at 08:44, *"Now, I can also consult
  the heat map and see whether these bars were really thick or not. Yes."*
- to beginners (09:18): *"heat map, yes, you can use it if you don't have such a
  deep understanding of the markets"*
- he uses it himself (11:46) to *"predefine certain levels… where the market
  might move to"*

His claim is about **sufficiency**: *"heat maps are cool if you're starting to
look at a lot of markets… not a good way to build an edge"* (14:52). Against
Carmine's ep. 3 the disagreement is real but is about emphasis, not use.
**Fixed on the card, in the sweep, and with a cross-note on ep. 3's card.**

**2. Class 4 — an "internal inconsistency" that does not exist.** The card said
he is firmer about spoofing here (*"illegal"*) than in `vl01TiVTuoQ` (*"probably
still"* around). He says the same thing in both: *"which by the way is
absolutely forbidden. Nevertheless, it does happen sometimes."* "Illegal" was
Gemini's word. **Fixed** — the flagged inconsistency withdrawn.

**3. Class 2 + a dropped qualifier.** *"or 400, 500, 600"* was quoted; he says
*"If you know it has 500 contracts, 400, 600, then you know it's really big"*.
More importantly the card dropped *"isolated and on its own"* — the 250–300
threshold is for a **single standalone order**, not aggregate depth. **Fixed.**

**4. Class 3 — spoken instruments rendered as on-screen strings.** The DOM
array `ZM, CL, Russell, Nasdaq, S&P 500, FDAX` was set in code font from a
`verbatim: null` visual claim. They are **spoken** at 04:18–04:23, and
introduced as volume profiles per market, not only DOMs. Also "20 levels by
default" is his current setting: *"we currently have 20 orders visible… You
just have to set it up yourself"*. **Fixed.**

**5. Omission that cuts against another of our claims.** The card never
recorded 05:13 *"it is true that a market seeks liquidity"* or 10:23 *"the
market… actually grabs the big liquidity. But there are also phases where the
market just ranges."* The same channel's podcast calls stop-hunt and
liquidity-sweep narratives a retail myth. **The channel does not flatly deny
liquidity-seeking; it denies that it is always the operative regime.** Added.

**6. Correction to a convergence count.** The sweep credited iceberg orders as
"three independent arrivals — `Vd83oo_geMk`, Carmine ep. 2, Trading Notes". The
word appears **nowhere** in ep. 2's transcript or card. It is **two**; Carmine
has absorption, the same mechanism unnamed. **Fixed.**

---

## 2026-09-06 · `vl01TiVTuoQ` — Vorwald, order-flow guide · **class 1, 2, 4, 5**

**1. Class 2 — the flagship definition is not verifiably verbatim.** The card
labelled this "spoken at 00:42, verbatim", and the sweep quoted it as the
corpus's cleanest one-line definition of order flow:

> Gemini: *"…but who is **currently** buying, who is **currently** selling…"*
> Captions: *"…but who's buying, who's selling, and how aggressively."*

Two machine transcriptions of AI-dubbed audio, no frames, and they disagree.
**Neither is authoritative.** Both card and sweep now carry the caption wording
with the discrepancy noted. The sense is unchanged; the "verbatim" label was
not earned.

**2. Class 4 — an unresolved digit.** The DAX ladder is carded `1, 1, 2, 4, 3,
5, 33`. Captions hear eight digits: *"1 1 2 4 3 5 3 3"*. No frames exist. Now
recorded as unresolved; a five-second frame pull at 04:00 would settle it.
**Settled 2026-09-08 by frames** (`videos/vl01TiVTuoQ/frames-356-408/f_0007.jpg`,
≈04:02): the FDAXM6 ask column reads 1, 1, 2, 4, 3, 4, 5, 3, 3 upward from
25152 — every level single-digit, the "33" a joined pair. Card corrected; the
sweep's ladder sentence is now out of scope (EDITS.md 2026-09-08).

**3. Class 1 + terminology.** "Level 3 showing up to 100 orders deep" drops the
hedge that immediately follows — *"**I don't even know exactly how many** you
can have displayed"* — and endorses his loose usage. What he describes is a
deeper **Level 2** display (the same 20-settable-to-100 rows as `Vd83oo_geMk`);
vendor "Level 3" means order-by-order data. **Both fixed.**

**4. Class 2 — a spliced quote.** The spoofing line was compressed across a cut
and lightly rewritten ("They're usually real" → "are usually real"). Full
wording restored.

**5. Class 4 — a slogan put in his mouth.** "Candlesticks are guessing,
footprint is knowing" is Gemini's inference from a `verbatim: null` claim. He
says *"Everyone knows these charts, but hardly anyone knows these. And that's
exactly the difference between guessing and knowing"* — naming neither. **Fixed.**

**6. Class 5 — a platform guess.** The German execution panel was called
"StereoTrader-class". The run's own note says the layout resembles ATAS/Sierra
Chart, and the identical panel (`Schließen`, `Kauf MKT`) is identified as the
**ATAS DOM Trader** on `yWO8hVpRXeY`. **Corrected to ATAS.**

**Omissions now in the read:** two spoken size references absent from the
card's calibration table — crude oil *"a 100 block"* (04:34) and a hypothetical
*"like a 300, 250"* (05:31), the latter independently restating the ES
threshold from `Vd83oo_geMk`.

---

## 2026-09-06 · `RwQBdF9TSvc` — Vorwald, the ICT-rejection podcast · **class 1, 2, 4**

All 13 run claims are `verbatim: null` — there is no on-screen text in this
video — so every quoted string in the card was Gemini's wording.

**1. Class 2 — a quote that was never spoken.** The card and sweep both carried
ICT narratives as *"hyped up and inaccurate"*. **"Inaccurate" is never said.**
He says the ICT strategy *"is being hyped up a lot"*, that *"people always talk
about how the banks supposedly always sweep the stops"*, and rejects it as
*"It's not true that there's any kind of stop hunting going on"* (04:12) /
*"it's nonsense to claim that"* (05:46). **Fixed in both.**

**2. Class 2 — "a retail trading myth".** "Retail" is not spoken: *"this myth
that the big players are always… hunting or fishing for stop-losses isn't
really how it is out there"* (02:27). **Fixed.**

**3. Class 4 — an agreement filed as a conflict.** The card and sweep had S/R
*"do not truly exist as fixed price points"* set **against Carmine ep. 5**. The
sentence immediately before (19:18–19:44) defines what does exist: price
reaches a level, trades actively, holds, the market moves away — *"then for me
that's when it **truly becomes real support and resistance because the market
confirms it for me**"*. That is ep. 5's validation thesis. The real
disagreement is **point versus area**, not existence. **Refiled as a
convergence with a caveat.**

**4. Class 4 — the distance from Trading Notes was overstated.** "This channel
says the effect is largely not there at all" is wrong: the podcast **concedes
the mechanical stop-out** (*"that's a normal principle that positions have to
be closed accordingly in those situations"*, 20:22–20:32) and that a large
candle means *"there was liquidity further down and it got filled there"*
(28:04). It denies **agency**, not the effect. **Fixed.**

**5. Class 1, three mild hardenings.** *"Routinely"* for *"often… sometimes"*;
*"up to 80%"* for *"sometimes 80%"* (an instance recorded as a ceiling); and
the 10,000-contract observation stripped of its hedge — *"you don't know
exactly… it could also be 10,000 individual traders."* Also corrected: that
figure was called "an order of magnitude above" the 250–300 threshold, but the
two are different quantities (executed versus resting) and the ratio is 33–40×.

**Clean:** the DAX 20-point spreads, Euro Stoxx 300–500 to single digits, the
2006–2008 anecdotes, and the absence of on-screen text. The card names no
speaker, correctly — the captions do not separate them across 25:06–27:22.

---

## 2026-09-06 · `jXR1afMy-3o` — Vorwald, PbD explained · **class 1, 2**

**The finding that matters beyond this card: Gemini translates German slides
into English and returns the translation in the `verbatim` field.** Proven
inside one run — the 00:19 German slide is reported correctly in German, then
the same slide at 09:05 comes back as an English "verbatim" string. On this
channel `verbatim` is evidence of *meaning*, not of *wording*. Written into
LESSONS.md; it downgrades an evidence class across all 21 Vorwald videos.

**"Break-in" is now provisional vocabulary.** The corpus had adopted it as the
name for a failed breakout. The crisp definition is Gemini's (`verbatim: null`),
he attaches the word to a different sentence, and — decisively — the audio is an
AI dub of German, where *Einbruch* (a plunge) would render as "break-in" too.
**A translation layer can manufacture terminology.** Caveated on the card and in
the sweep; not corpus vocabulary until frames settle it.

Also: the 05:15 candle-close line was set in quotation marks but is a
paraphrase, and what he says there is an *observation* — *"I very often see
candlesticks with closing prices"* — with the rule form arriving at 05:36 and
08:56. And platform/instrument (ATAS, FDAX) were stated flatly against the
run's own "partially obscured and low-resolution".

---

## 2026-09-06 · `usho6UVLqkE` — Vorwald, DOM & footprint · **class 2**

13 of 14 run claims are `verbatim: null`. The DAX ladder was carded in code
font as `2, 4, 8, 11, 7`; he speaks **six** values — *"two contracts, four
contracts, four contracts, eight contracts, 11 contracts, seven contracts"*.
Gemini compressed, the card set it as if read off the screen, and the sweep
repeated it. **Fixed in both.** `WORLD CLASS EDGE` in backticks likewise comes
from a `verbatim: null` visual claim, and "712 market orders sold **at one
price**" should be *"into the previous price range"*.

**A cascade I missed:** the iceberg count was corrected to two in the sweep but
left at "third independent arrival" on `Vd83oo_geMk`'s card and READ. **Now
fixed.** Same failure as before — fixing one copy of a claim that lives in
several.

---

## 2026-09-06 · `yWO8hVpRXeY` — Vorwald, the live DAX trade · **class 1, 4**

**The sweep's "one executed trade" was over-read, and the over-read was mine.**
Card and synthesis both said: *"74 / 23 = 3.22 R realised, closing against the
stated ~1:3 target… the only place in the sweep where a stated risk, a stated
target and a realised outcome appear together and reconcile."*

The transcript does not support any of the three:

- **No target is stated anywhere in the video.** The *"good 1:2"* (04:51) and
  *"almost three"* (10:00) are **running open-profit multiples** called out as
  the trade moves — 62 points open against 23 ticks risked gives 2.7, which is
  what "almost three" means.
- **74 ticks is a floor, not a realisation**: *"we will definitely secure 74
  ticks for ourselves"* describes where the trailing stop sat. The close at
  17:18 — *"The market pushed down, hit the limit"* — carries **no figure**.
- The entry fill, contract count and any take-profit are **never spoken**.

Also merged under one timestamp: the stop rule at 03:47 (*"above the
structure"*) and the breakeven refusal at 06:22 (*"This isn't a 'let's move the
stop loss to zero' situation"*), with "arbitrarily" being Gemini's word; and
three separate stop tightenings (14:03, 14:20, 15:50) folded into one row.

**What survives** is still unique in the sweep and worth having: a stated risk
(23 ticks), a real ATAS execution panel, and a locked-in floor — the only video
of 21 to show any of it. It is simply not a closed, reconciled trade record.
**Fixed in the card and the synthesis.**

---

## 2026-09-06 · `uFxYcpiaOpw` — Vorwald, the 80–90% claim · **class 1, 4**

**Third cascade miss, inside a card I had already corrected.** Findings used
the corrected *"maybe a two"* wording while the Lessons bullet still read
*"present (as >2) only in NkQeOVDTAec"*. A repo-wide grep now returns zero.

**The close-rule attestation is weaker than carded.** He says *"I have a
breakout here with this higher closing price"* (07:13). The closing price is
spoken; *"consolidation level"*, the wick contrast and *"explicit"* are
Gemini's. The synthesis now records that the four attestations are **not
equal** and names where the strong ones are (`jXR1afMy-3o`).

**"Break-in" gets worse.** At 07:09 the dub says *"this **break-in** happened
right here"* one sentence before *"I have a **breakout** here"* — **for the
same move**. German *Ausbruch* and *Einbruch* are being rendered
inconsistently, so the word carries no stable sense in this corpus.

Also: instruments *"ES and Nikkei 225 mini"* come from a chart title Gemini's
own uncertainties call *"tiny and partially compressed"* — he says only *"the
Nikkei future"*; the on-screen `Once a day` drops the spoken hedge *"about"*;
and *"ATAS inside MS Paint"* is a `verbatim: null` visual claim stated as fact.

**Break-even arithmetic confirmed** independently: 0.25 at 80%, 0.111 at 90%;
adding our measured 0.17 R of ES friction lifts those to 0.46 and 0.30.

---

## 2026-09-06 · `m3IMdc7QwN4` — Vorwald, the PbD key · **class 1, 3, 4**

**The most consequential correction of the run: PbD is "phases", not
"shapes", and the shapes gloss is ours.**

His only expansion, 07:44–07:55: *"the D's are nothing more than large
**balance phases**. The P's are the aggressive **trend phases upwards**, and
the B's are the aggressive **trend phases downwards**."*

Card, synthesis **and the composer brief** all said the letters are the
**shapes** a TPO distribution draws, presented as his expansion. It is a
defensible reading — at 04:57 he attaches *"That means a B"* at the moment the
lower balance forms *after* the sell-off, and sibling videos draw the letters
by hand — but it is **our** reading. Fixed in all three, attributed to us. Two
further copies inside this same card (Sessions verdict, Lessons bullet)
survived the first pass and were fixed on a follow-up grep — the **fourth**
cascade miss of the run.

Also: *"annotation in MS Paint as usual"* is channel habit, unevidenced here;
Sierra Chart and ES were stated flatly against a `verbatim: null` claim whose
own uncertainties call the header *"partially compressed and low resolution"*;
*"on this slide Nill is second"* is inferred rather than read (the capture has
no rank digit and is not sorted by return); and what he **says** at 00:15 is
*"the two-time World Cup Championships of trading **leader**"* — leader, not
champion.

---

# 2026-09-07 · second composition run — 27 reads, central reconciliation

Twenty-seven composers (12 Vorwald, 10 SMDX, Trading Notes, AlgoTrade Pro,
the AI video, two Trader Dale) reported; three frame pulls settled the
load-bearing disputes. Substantive corrections applied to cards and syntheses
on this date; minor class-1 hedges are logged here and left in the cards where
the substance holds.

## `1utSjHs_Mq8` — Vorwald, market profile · **class 4, 5** · FRAMES
- **Instrument.** Card said `6E` Euro FX (one run's visual). Spoken levels
  6,714 / 6,758 are S&P levels; `frames-005-120/f_0002.jpg` shows a Sierra
  Chart header on CME dated 2025-10-22. **Fixed**; the Lesson "not index-only"
  withdrawn.
- Class 5: "weak highs created by *retail*" — 09:34 says *"weak traders"*.
  Propagated to the sweep and `5qBo04SMUFc/READ.md`. **All three fixed.**
- Class 1/4 minor: value area "roughly 70% … or time spent" — 13:11 "where
  70% of the trades took place". Logged.
- Omission: buying tail = "at least three distinct letters standing completely
  alone" (09:02).

## `K8qtT2_axPo` — Vorwald, market profile hub · **class 2** · FRAMES
- **Platform.** Card's backticked `Powered by VolFix.net` was `verbatim:
  null`; the fallback run read "shiftnest". `frames-012-040/f_0006.jpg`
  (00:22): header `ESH26-CME [CBV][M] #4 … TPOs: 1.25 x 30 min · 2025-12-18`,
  axis 6,780–6,960, no watermark. Platform is **Sierra Chart**, screenshots
  in HyperSnap 8; instrument ESH26. **Fixed** in card, Lessons and the sweep.
- Class 4/5 minor: "initial balance = opening 30 min | 02:55" (term at 07:31);
  "time vs volume | 02:15" (content at 05:35, 14:08). Logged.
- Class 1 light: ledgers "weak hands" drops 13:38 "or have held it up".

## `VumVuGnCcFM` — Vorwald, VWAP · **class 1, 2, 4, 5** · FRAMES
- `>20%` IS on the canvas (`frames-940-958/f_0009.jpg`, ≈09:56); spoken as
  "about 20% of trading days for many products". Card **confirmed and
  annotated** with both.
- Class 1: "invalidating mean-reversion" — 08:00 "caution is advised". Logged.
- Class 2/4: "liquidated during a runaway trend" — 11:06 "some news comes out".
  Logged.
- Class 5: "institutional participants" — 04:04 "large market participants".
- Cross-ref: "identical to 43JaKHRvxHk's Rule 1" — matches that video's 06:30
  balance rule; the Rule-1 match is this video's 11:43–11:49. **Fixed.**

## `YkclL6xgu-s` — Vorwald, volume · **class 1, 2, 4, 5**
- **Class 1, important.** "600 vs baselines of 800 and 1,000 on previous
  days" — 02:40 *"just imagine … 800 … maybe you even had 1,000"*. Hypotheticals
  recorded as observed baselines, in Findings and Sessions. **Fixed.**
- Class 2: stop "below the prior established volume consolidation block" —
  12:06 "below the last volumes". Logged.
- Class 1: weekly signal "signals" — 08:23 "higher likelihood"; the
  low-volume condition dropped; timestamp 06:19 → 08:21. Logged.
- Class 4/5 minor: POC definition at 07:06 not 05:40; "ES, FDAX, CL" are our
  tickers for "S&P future, DAX future or crude oil".

## `HySZZSjMxF8` — Vorwald, multi-timeframe hub · **class 1, 5**
- **Class 1.** "No candle close is required" — 10:43–10:52 never mentions a
  close; the wording was Gemini's `verbatim: null` inference. **Fixed.**
- Class 5: he names option two *"a really nice B structure setup"* (09:18);
  unrecorded. **Added.** "Fakeout wick" was Gemini's. **Fixed.**
- Class 5 minor: "balance phase" for his "sideways".

## `zAwEX_tRUfE` — Vorwald, 1-minute scalping (ES) · **class 1**
- "Requires no confirmation at all beyond the break" — 03:41–04:09 names
  acceptance / a stable balance above the level. **Fixed.**
- "'Accumulation' … is absorption in Carmine's vocabulary" — 06:24 describes
  initiative buying establishing acceptance; the gloss was ours. **Fixed.**
- Minor: "computed once", "no indicators at all" are compression. Logged.

## `aursfDVYzUk` — Vorwald, entry with volume · **class 1, 2, 5**
- Name set in quotation marks was `verbatim: null`; captions say "Polvald".
  **Fixed** (fourth rendering, name stays unresolved).
- "Institutions *need* 1.5–2 days … mechanism behind composite profiles" —
  03:13 "sometimes … depending on which instrument"; mechanism ours. **Fixed.**
- "Dismisses the *retail* stop-loss waves" — concedes the stop-out at 09:35,
  rejects the label; "retail" never spoken. **Fixed.**
- "68.2% is one standard deviation" — 06:30 "68.2 or 70%"; SD gloss ours.
  **Fixed.**
- Omission: 07:56 "70% of the time we are in stable market phases".

## `Ly62G168MkQ` — Vorwald, PbD beginners · **class 2, 5**
- P-profile "consolidation near the highs — confirming the shape reading" —
  06:46 "a market imbalance on the buy side"; shapes gloss is ours. **Fixed.**
- Class 2 minor: 05:10 "confirm acceptance" is Gemini's wording; substance OK.
- Class 3-adjacent: "70% in green ink at 15:46" rests on a null-verbatim
  visual; spoken "about 70%" at 15:43. Logged, unframed.
- Class 1 minor: Lessons generalises "DAX and Gold on 1-minute" from one video.

## `43JaKHRvxHk` — Vorwald, VWAP wrong · **class 1, 5**
- Two-mode summary (trend = pullback / balance = target) is our compression
  of three uses at 08:12–10:11. **Fixed.**
- Minor: Rule 1 "pull-back" glosses the dub's "counter trades"; "classify the
  open first" — 04:44 "for example"; "strictly the current day" — 01:50
  "usually". Bands 0.5/1/1.5/2 from a truncated study bar, unframed. Logged.

## `YmygDgtoxO8` — Vorwald, volume profile · **class 1, 2**
- "Explosive breakouts occur" — 11:47 "probability … is very high", and the
  12:08–12:24 counter-case dropped. **Fixed.**
- Mild: base rate 05:36 conditional and "typically"; "explicitly departs from
  convention on POC" — 06:58 "a bit differently". Logged.

## `Kg6sYKgtkrY` — Vorwald, 2026 strategy · **class 1, 2, 4**
- "Six markets" — five charted. **Fixed** (Sessions).
- Class 2: "what market profilers call" single prints — 02:45 "would *partly*
  call"; "thin vertical price movement zones" is Gemini's. Logged.
- Class 1/4: "6900 as lower *profile* boundary" — 09:44 "lower boundary".
  Logged.

## `0CrkbfuIhkc` — Vorwald, crash or all-in · **class 1**
- "The only place in the sweep where he ties a level to a closing price" —
  the sweep lists four others. **Fixed** (Findings and Sessions).
- Minor: "MS Paint drawings (03:14)" asserted where the run hedged the tool;
  the 6,850 → 6,300 → 4,600 table drops the "with liquidity" condition and
  the "high probability / for now" hedges (03:54–04:35). Logged.
- "Break-in" third instance at 09:45 (Google) — cut for scope.

## `GGe2widuvPs` — SMDX, mechanics · **class 4**
- Card blamed the "$90" caption for a "$140" drawn gap; narration says the
  next sell order is at $50,100 (03:40–04:02), so the caption is right and
  the drawing is off. **Fixed** in card (three places) and SMDX synthesis.

## `UL5QOCSKnU0` — AlgoTrade Pro backtest · **class 2, 4**
- "Presented as givens with no account" — 02:14 "keeping the defaults".
  **Fixed.**
- Pro Tip "no number" — 06:07 "win rate jump by 3 to 5%". **Fixed.**
- Settings row `2 ATR PIP VALUE (Both Stop Loss & Profit Target)` and the
  SPX500 rows (5-min `99.46 | 23.77 | 49.08 | 491`, two runs) were absent.
  **Added, unframed**, with the note that the ATR stop would undercut the
  card's swing-stop cost arithmetic.
- Class 2 minor: MTF panel defaults claim is `verbatim: null`.

## `iPDi9_nzn-o` — SMDX ChoCH · **class 4**
- "1–2 candle snap-back" is the slide; spoken 09:15 "one to three", 09:22
  "one or two". Logged.
- "Not specified: stop/target" — the stop is on screen at 11:53 (frames).
  **Fixed** (target only).
- Source error flagged in the read: 12:27 "stops = sell orders, institution
  fills short" inverts the mechanics (absorbing sells makes you long).

## `sASTlqfPg-8` — AI video · **class 1, 4**
- "Zero debt" is the slide; narration "minimal debt" (03:15–03:24). Logged.
- "Synthesis of Schwager's Stock Market Wizards" — never named; title card
  only. "Horizon of months to years" — never stated. Both inference stated
  as observation. Logged; card verdict stands with that caveat.

## `dAlP8UZXT48` — SMDX structure · **class 1 borderline**
- "ChoCH = first warning" drops 07:15 "multiple changes of character in
  sequence are a trend reversal confirmed". Logged.

## `EW_TtV_rgzY` — SMDX timeframes · **class 1 soft**
- The card frames slide text as the rule where the speech hedges ("one of the
  most costly", 03:01; "most of the setups", 11:21). Logged.

## `7F9wBYse-Nk`, `Ex5Dk_wVygw`, `YwqfGuktXrc`, `d2RzSJC98o8`, `jb6Odrq6alA`,
## `oktlv1rOG9Q` — SMDX · **clean**
- Source-level notes only: slides harden the presenter's own spoken hedges
  (YwqfGuktXrc 05:36; d2RzSJC98o8 06:06); d2RzSJC98o8 06:55 "at least two
  candles" vs 05:03 "three to five"; 7F9wBYse-Nk institution list differs
  between slide (03:14) and narration (03:05). Mock charts are BTC/USDT
  (Lessons candidates for scope).

## `IUWvHVout94` — Trading Notes · **class 2, 4, 5**
- "Never says whether the structure shift needs a close" — 12:53 *"it does
  it on candle closes, exactly like our rule"*, inside the Flux Charts demo.
  Gap narrows to "stated only in the sponsor segment". Logged; grade reasoning
  should reflect it.
- Liquidity definition set as a quote was a stitched `verbatim: null`
  paraphrase; "retail stop losses" — "retail" never spoken; "ChoCH" spoken
  only in the demo. Logged.
- Unrecorded inconsistency: the worked example enters *on the sweep*
  (`STEP 3 ENTRY ON SWEEP`, 09:27), contradicting step 3 and Mistake 3.
- Cascade found by the composer: `Vd83oo_geMk/CARD.md` still says "third
  independent arrival" on icebergs; the brief says two. **Checked below.**

## `vVMJa7dyYWE`, `8O_GIxjhLkc` — Trader Dale (cards written 2026-09-07)
- Pitch span 29:51–36:42 was stitched from two slide timestamps; the pitch
  is 29:51–31:25 and 32:05–36:41 is a quiz with method content. **Fixed.**
- "Roughly 70% … rotation" in quotation marks was a paraphrase of *"I would
  say like maybe 70%"*. **Fixed.**
- ES short: entry-criteria list, the dark-ring sentence and the "Academy
  membership" pitch were paraphrases or inferences. **Fixed** with the
  transcript wording.
