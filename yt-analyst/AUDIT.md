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
