# Brief — the reading UI

Guidance for the next task: designing and building a reading interface over the
yt-analyst corpus. Written 2026-09-07 at the end of the composition run, while
the reasons behind the decisions are still recoverable.

Steve's two choices, already made: **explore directions in `/design` first,
then build the real thing as an Artifact**, and the primary job is **reading
the corpus** — not presenting it, not working the claims.

---

## 1. The thing that should shape the design

The corpus was built in two layers, and the second one audited the first.

`CARD.md` is machine-facing: dense, timestamped, provenance-marked. `READ.md`
is human-facing, composed **from the video transcript** rather than from the
card, because the card is a lossy compression that had already discarded the
presenter's voice, examples and explanations. You cannot decompress good
reading out of it.

Composing the reads found **~75 errors in the cards**. Not one was a fabricated
number. Every substantive one was **compression that hardened**:

| Recorded | Actually said |
|---|---|
| "PbD = the **shapes** a TPO profile draws" | *"the D's are… large balance **phases**"* — and the shapes gloss was **ours** |
| Professionals *"do not rely on heatmaps"* — "the sharpest conflict in the corpus" | *"such a wonderful tool"*; he demonstrates it on screen. Sufficiency, not rejection |
| S/R *"do not truly exist"* — **against** Carmine ep. 5 | *"…because the market confirms it for me"* — the same thesis. An agreement |
| A live trade where risk, target and outcome "reconcile at 3.22R" | No target is ever stated; 74 ticks is a trailing-stop **floor** |
| "Target average risk-reward **> 2**" | *"maybe a two"*, inside a worked example |

**The design consequence.** Progressive disclosure is not a nicety here — it is
the mechanism that keeps the top of the document honest. A reader must be able
to drop from any claim in L1/L2 to the presenter's own words in L3 in one
gesture, because that is exactly the move that caught every one of these.

Build for **claim → evidence in one click**, and the UI inherits the discipline
that produced the corpus.

---

## 2. What exists

| Artifact | Count | Notes |
|---|---|---|
| `videos/<id>/CARD.md` | 43 | agent-facing record of truth; feeds `yta.py export` and sibling zgents |
| `videos/<id>/READ.md` | **18** | human-facing, four levels; 12 remain uncomposed |
| `videos/<id>/transcript.txt` | 43 | substrate; gitignored, regenerate with `fetch_transcripts.py` |
| `playlists/*.md` | 3 | two order-flow syntheses + SMDX |
| `AUDIT.md` | 556 lines | every correction, by failure class, with what propagated where |
| `corpus.json` | generated | the data layer — `python3 build_corpus.py` |
| `.compose-brief.md` | — | corrected corpus facts, read by composers |

Corpus: **43 videos, 7 channels, 11h38m, 2024-10-14 → 2026-09-05, 171 runs.**

### READ.md structure and real dimensions

```
# Read: <title>
> **L0** — one line, 30–40 words
- Channel · Uploaded · Duration       (metadata bullets)
- Card: [CARD.md](CARD.md) · Watch: <url>
## In brief        L1  — 153–203 words, median 166
## The argument    L2  — 599–1,561 words, median 800; cross-links inline and named
## In his words    L3  — 924–5,627 words, median 3,113; quoted passages with
                        timestamp anchors, interleaved with editorial asides
```

- **Editor asides** are marked `> **Editor —** …` inside L3. 6–16 per read,
  median 12. They must render visually distinct from the presenter's quotes —
  this is the single most important typographic requirement.
- One read uses `## In their words` (a two-speaker podcast). Handle both.
- **L3 length varies 6×.** A layout that only looks right at 3,000 words will
  break at 900 and at 5,600.
- Total per read: 1,751 – 6,667 words, median 4,172.

---

## 3. Facets — what is dense and what is not

**Dense, safe to build on (43/43):** channel, title, upload date, duration
(and `duration_s`), **views**, status, run count, section names.

**Sparse, do not make primary:**
- **Grades: 5 of 43.** Only the bespoke-graded videos carry Clarity/Alignment.
  A grade column would be mostly empty.
- `bead`: 24/43. `playlist`: 37/43.

**Views are skewed and interesting.** The two most-viewed items in the corpus
are Vorwald volume-profile explainers at **314K** and **236K** — an order of
magnitude above the Carmine series we treated as canonical. Worth surfacing.

---

## 4. The link graph is real content

`corpus.json` carries **46 edges** between cards, with `links_in` / `links_out`
per card. Hubs: `HySZZSjMxF8` (5 inbound), `IUWvHVout94` (4), `K8qtT2_axPo` (4).

These are not "see also" decorations. A large share are **amendments** — one
card correcting another's finding, sometimes reversing it. The linked-notes
direction Steve picked is the one that uses this, and it is the only structure
in the corpus a generic video index would not have.

**Suggested treatment:** show inbound links as marginal annotations while
reading, not as a footer list. "Three cards refer to this passage" is the
interesting signal; a bibliography is not.

---

## 5. Evidence grades — carry them into the UI

Claims in this corpus are not equally supported, and the corpus now says so
explicitly. In descending order:

1. **frame-verified** — pixels checked. The strongest, and rare.
2. **two-source cross-check** — e.g. a pixels-only and an audio-only pass
   agreeing, or arithmetic closing against transcribed figures.
3. **arithmetic** — figures satisfying independent relations.
4. **spoken / unverified** — recorded as said, not checked.
5. **`verbatim: null`** — Gemini's *paraphrase*. Never a quote.

Two hazards worth encoding as UI affordances rather than prose:

- **A `verbatim: null` claim reads exactly like a quotation** and normalises
  hedges. Anything the UI renders in quotation marks should be traceable.
- **On the German channel, Gemini returns translations in the `verbatim`
  field** — proven within one run. An English "verbatim" on a German slide is
  evidence of meaning, not wording.

---

## 6. Corrections are content, not clutter

Cards carry **20 correction annotations** (`Corrected 2026-09-06`, `AMENDED`,
`CORRECTED`), and `AUDIT.md` holds the full trail by failure class.

Resist hiding these. A reader who can see *"this card previously said X; the
transcript says Y"* trusts the rest more, not less. At minimum, make
`AUDIT.md` reachable; better, mark corrected passages inline and let the reader
expand the history.

---

## 7. Design constraints learned the hard way

- **Artboards are sandboxed iframes.** Browser zoom cannot reach inside one, so
  Ctrl+wheel and Ctrl+± will not work in `/design` previews. Judge the
  directions on typography, hierarchy and density; interaction comes with the
  Artifact.
- **`browser.html` already exists** (`yta.py browse`) — a sortable,
  source-filterable table of all 43 cards. It is the thing being replaced.
  Its weakness is the diagnosis Steve made: it shows agent-facing text.
- **Author the Artifact page in HTML**, load the `artifact-design` skill before
  writing it, and load `artifact-capabilities` first if the page should persist
  anything (read-state, filters, notes).
- Content is markdown. A renderer already exists in `yta.py`'s `browse`
  template and was hardened against real card content — two bugs worth not
  rediscovering: a line starting with `|` is only a table when a separator row
  follows, and emphasis matching must not eat literal asterisks that are
  transcribed screen glyphs.

---

## 8. What is not done

- **12 READs remain** (listed below). They are mostly profile explainers that
  overlap heavily; the 18 written cover every distinct *kind* of video in the
  corpus — long teaching series, live trade, visual-free podcast, dense options
  maths, a bold statistical claim. Adequate as a design sample.
  `0CrkbfuIhkc · 1utSjHs_Mq8 · 43JaKHRvxHk · HySZZSjMxF8 · K8qtT2_axPo ·
  Kg6sYKgtkrY · Ly62G168MkQ · VumVuGnCcFM · YkclL6xgu-s · YmygDgtoxO8 ·
  aursfDVYzUk · zAwEX_tRUfE`
- ~~`build_corpus.py` does not yet read `READ.md`.~~ Done 2026-09-07: each card
  carries `read` (L0, L1/L2 markdown, L3 passages with timestamps, asides as
  their own list, word counts), `audit` entries from `AUDIT.md`, a
  `corrections` count and `verification` mark counts. `build_reader.py`
  assembles `reader.html` (the Ledger interface) from `reader.template.html`.
- Frame pulls that would settle open questions: the `$208,000` vs `$28,000`
  overlay (Carmine ep. 1, 00:01–00:08), the DAX ladder's last digit
  (`vl01TiVTuoQ` 04:00), and whether "break-in" is a term or a dub artefact
  (`jXR1afMy-3o` 09:45–10:20).

---

## 9. If you compose more reads

Follow `.claude/skills/composing-card-reads/SKILL.md` and hand every composer
`.compose-brief.md`. Two rules earned in this run:

- **The card audit is half the job**, not a side note. It found ~75 errors,
  including in claims the parent session had reported as findings.
- **Grep after every correction.** Four times in one run a claim was fixed in
  one place and left standing in its own card's Sessions verdict, Lessons
  bullet or a synthesis table. Importance predicts cascade risk, because
  important claims get stated twice.
