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
