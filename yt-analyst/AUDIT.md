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
