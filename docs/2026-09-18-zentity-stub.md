# Zentity — the stub a conventional architect would hand you

Draft for Steve, 2026-09-18. Not a canon and not a ruling.

This is the shape a working software architect would put on the table on day
one. The slots are filled from what the enterprise already holds. The job in
front of you is editing and deciding, not authoring from nothing.

Its home, once adopted, is COO. It sits in DReader because that is where it was
written; nothing here is DReader's to rule on.

---

## 1. Where this thread actually stands

You are not starting. You are resuming, and more is on the record than the
scattered state suggests.

- **You coined the word** in Claude Desktop on or after 2026-08-13. The raw
  conversation is **lost** — no transcript, no bead store, no memory holds it.
  What survives is Desktop's own write-up, which COO recovered from a browser
  cache on 08-16: `COO/myDesk/reports/claude-desktop-recovered/zentity-addendum.md`
  (co-8xne3, desk page `desk-zentity-addendum`).
- **You declined a `zentity-discipline.md` draft** at the time. The stated
  reason, from the addendum's closing: *"The Zentity concept is now named in
  enterprise vocabulary; future work will develop it through COO with Steve's
  background properly hydrated, not through Claude improvising from partial
  memory in an isolated session."* **This document is that hydration being
  asked for.** The parking was deliberate and the condition for resuming it is
  the one you just named.
- **Two definitions are on record, both yours.** COO reads them as one thing
  seen from two sides, and I agree:
  - the **decoration** cut (addendum): *"a Zentity is something built by
    decoration of an existing something — taking a base object model (an
    external API, a forked codebase, an adopted tool) and layering your own
    features onto it. The Schwab API is a Zentity once you've forked and
    extended it. Every fork on the fork-ownership ladder is Zentity work."*
  - the **ownership/composition** cut (to Strader, 08-18): *"an entity that we
    own. An object model that interacts with other of our object models."*

  The first says how a thing *becomes* one. The second says what it *is* once
  it is ours.
- **One hard rule is already settled:** Zentity is **not** a superclass of
  zgent. Desktop proposed "zgent = active Zentity" to tidy the type system and
  you rejected it. The Z/z capitalisation is doing semantic work.
- **One worked example is already built:** the Playbook entity in Strader —
  identity, provenance, curation status, controlled-vocabulary conditions,
  checklists, a catalog and an evaluator. COO's framing of it is the sharpest
  sentence anyone has written on this: *"the contract is the Zentity and the
  strategies are data conforming to it."*
- **One header standard is already in use:** OKF (Open Knowledge Format, the
  typed front matter on every knowledge file), extended, and read as data by
  `Strader/strader/entities/canon.py` — `id`, `type`, `status`, `owner`,
  `provenance{origin, ref}`, `sources[]`, `lineage{supersedes, since, commit}`,
  `cite[]`. Thirty-three knowledge files and nine playbook records are being
  migrated to it (st-ts3o).
- **Eleven entities were already normalised** in Strader's trade-language
  survey (2026-07-25, st-79z.1): Level, Trigger, Setup, Regime/DayType,
  SessionWindow, Intent, StructureTemplate, Order, Bracket, Size/Risk,
  Position — each carrying explicit **provenance**, and anything priced
  carrying an explicit **price-frame**, because the absence of exactly those
  two attributes caused two real vocabulary incidents.

So the record holds two definitions and one hard rule. It holds one worked
contract, one header standard and one eleven-entity survey. It also holds one
empty registry — `COO/entities.json` carries `"people": []` and seven bare
project strings. The parts exist. Nobody has put them in one place.

## 2. On the limitation you named

Worth saying plainly, because it bears on how to read everything below.

You said two things. You haven't been on an architecturally-oriented team
defining higher-order constructs. Your success has come from bringing cohesion
to disparate parts.

The addendum records your own account of BankWebinars: *"The BW UI worked
because the entities were done right — the rich object model came first, the UI
emerged from it."* That is thirty years of exactly this work.

What you are missing is the **vocabulary and the artifact shapes**, not the
judgement. The vocabulary is about four hours of reading. The judgement is the
part nobody can hand you.

The instinct you describe as your strength also has a conventional name.

When an organisation has five partial models of the same thing in five places,
the classical move is **not** to unify them into one global model. It is to
name each context, say which model holds inside it, then define the translation
at each seam. That is context mapping. It is the senior half of this
discipline, and your instinct is already pointed at it.

## 3. The frame — what any entity definition has to answer

A conventional architect would refuse to call something an entity until these
are answered. Use this as the interrogation for every candidate.

| # | Question | Failure if unanswered |
|---|---|---|
| 1 | **Identity** — what makes two references the same thing? | you get duplicates nobody can reconcile |
| 2 | **Boundary** — what is inside it, and what is merely related to it? | every change touches everything |
| 3 | **Authority** — who is the system of record; who may create, change, retire one? | two sources disagree and neither is wrong |
| 4 | **Lifecycle** — how does it begin, what states can it be in, how does it end? | nothing is ever retired, only abandoned |
| 5 | **Relations** — what kinds are allowed; is a relation itself a thing? | the model becomes a graph of "related somehow" |
| 6 | **Representation** — where does it live, in what format? | it lives in five formats and drifts |

**The working rule:** if you cannot answer 1, 3 and 4 for a candidate, it is not
an entity yet. It is an attribute, an event, or a report.

## 4. The distinction this draft must not collapse

This is the one place I would push back on the vocabulary as it stands, and it
is the most useful thing in this document.

**"Zentity" as you defined it answers *is it ours?*** It names a thing we took,
forked, decorated and now own, which composes with our other models.

**"Entity" in the conventional sense answers *does it have identity?*** — a
thing that stays itself when its attributes change. A bead is an entity: change
its title and it is the same bead. A price is not: change the number and it is
a different price.

These are **orthogonal axes**, and the enterprise currently has one word doing
both jobs. Keeping them apart costs one sentence and buys the whole model:

|  | **has identity** | **no identity (a value)** |
|---|---|---|
| **ours** | a Zentity, with entities inside it — Playbook, bead, zgent | a format we own — a fact sheet, a card grade |
| **not ours** | an external model we consume — Schwab's order, Databento's instrument | raw data — a tick, a frame |

Your decoration definition is then precisely a **transition across that
table**: something moves from *not ours* to *ours* by being forked and
decorated. That is why Zentity reads as a *discipline* rather than a taxonomy.
It names an act, not a category.

The addendum says as much: *"invest in entities for things that matter, accept
that early models will be broken and remade, count the breaking as part of the
cost of doing modeling well."*

**Recommended:** keep **Zentity** for the ownership axis, meaning what we own
and compose. Use **entity** plainly for the identity axis, which is what the
OKF header already describes. One word doing two jobs is how vocabularies rot.
The Mancini/Carmine level-provenance incident (st-1s1) is the standing local
proof.

## 5. The stub — the document to edit

> Everything below is a draft to strike through. **DECIDE** marks a slot where
> no answer exists on the record and the choice is yours.

### 5.1 Definition

> A **Zentity** is an object model this enterprise owns, usually arrived at by
> decorating something that already existed. It composes with our other owned
> models through a declared contract.

### 5.2 The test — a candidate qualifies when all four hold

1. **We own the contract.** Not the data, not the source: the contract. A
   stranger's strategy plugs into Playbook exactly as far as Playbook's fields
   reach.
2. **It has identity** that survives changes to its attributes, and that
   identity is written down somewhere stable.
3. **It has an authority** — one system of record, one owner who may create,
   change and retire it.
4. **It composes** — at least one other owned model refers to it by its
   identity.

### 5.3 What is explicitly not a Zentity

- a **zgent** (settled: Zentity is not a superclass of zgent; zgents are
  categorically more complex)
- a **value** — anything two of which, with equal contents, are the same thing
- an **event** — something that happened; immutable, timestamped, no lifecycle
- a **report or view** — a rendering of entities, regenerable, never a source
- a **file** — representation, not identity

### 5.4 Required fields — start from what already runs

OKF's extended header is already this, in production, read as data by
`canon.py`. Adopt it rather than invent:

```
id:           stable, kebab-case, equals the file stem
type:         OKF's field; the vocabulary grows, nothing is added beside it
status:       lifecycle state, from a closed vocabulary
owner:        the authority
provenance:   {origin, ref}      — where this came from, and the citation
sources:      [ids]              — registers this converges with
lineage:      {supersedes, since, commit}
cite:         [headings]         — required on method types
```

Add the two attributes the trade-language survey paid for in incidents. They
belong in the base, not in one repo's dialect:

```
provenance    on EVERY entity, not only knowledge files
price_frame   on anything carrying a price (ES vs SPX)
```

**DECIDE:** does a Zentity carry a `contract` field naming the shape data must
conform to, or is the contract implicit in `type`? *(Recommended: explicit —
Playbook's whole value is that its contract is inspectable.)*

### 5.5 Identity — **DECIDE**

Options, with the trade-offs a conventional engineer would state:

| option | good | bad |
|---|---|---|
| **natural key** (the file stem, the bead id) | human-readable, greppable, already true of OKF | renaming breaks references |
| **assigned surrogate** (a generated id) | survives renames | invisible in prose; nothing reads it |
| **both** — surrogate for machines, slug for humans, slug may change | best of both | two things to keep in step |

*(Recommended: keep OKF's natural key. It is already load-bearing and the
enterprise writes in prose more than it writes in code. Add a `lineage.supersedes`
discipline for renames — which OKF already has.)*

### 5.6 Relations — **DECIDE**

The enterprise already expresses relations three incompatible ways. Beads carry
typed dependencies: `parent`, `blocked-by`, `discovered-from`. Knowledge files
use `[[wikilinks]]` and `Related` lines. yt-analyst uses `{from, to, via}`
edges, 411 of them across 47 cards. Pick one shape for the base and let the
rest translate to it.

*(Recommended: `{from, to, kind}` with a closed `kind` vocabulary. It is the
simplest of the three. It is the only one already machine-read at scale. Both
others map onto it without loss.)*

### 5.7 The register — **DECIDE**

`COO/entities.json` exists and is empty. Either fill it or delete it; an empty
registry is worse than none, because it reads as an answer.

*(Recommended: fill it, and generate it from the sources rather than
maintaining it by hand. A hand-maintained registry is the same failure class as
everything in `DReader/docs/retired/REGISTER.md`.)*

## 6. The inventory — the cohesion work, which is yours

Every candidate visible across the enterprise today. Sorting this is the task
your instinct is actually good at, and it turns an abstract question into a
list. Columns are the frame's questions 1, 3 and 4.

| candidate | where it lives | identity today | authority | lifecycle | qualifies? |
|---|---|---|---|---|---|
| **bead** | `.beads/`, Dolt | `dr-`/`st-`/`co-` id | the repo it lives in | open → in_progress → closed/deferred | **yes** — the cleanest one we have |
| **zgent** | `COO/ZGENTS.md` | name | COO | certified / in-process | yes, but explicitly not a Zentity |
| **rig** | gc city | name | gc | registered/suspended | probably |
| **Playbook / strat** | `Strader/strader/playbooks/` | `code` | Steve, curated | candidate → worthy → … | **yes — the worked example** |
| **knowledge record** | `Strader/knowledge/` (OKF) | file stem | `owner` field | `status` vocabulary | **yes — already conforms** |
| **Level** | survey §3.1 | price + frame + source | the parse that produced it | per session | needs 1 and 4 |
| **Trigger, Setup, DayType, SessionWindow, Intent, StructureTemplate, Order, Bracket, Size/Risk, Position** | survey §3.2–3.11 | normalised on paper, not in code | unassigned | unassigned | **the survey did question 2; nobody did 1, 3, 4** |
| **capture / dossier** | `DReader/discord-reader/captures/` | `<timestamp>-<slug>` | DReader | open → closed → superseded | **yes — and it already has status** |
| **video card** | `DReader/yt-analyst/videos/` | YouTube id or chosen slug | DReader | open → closed → shelved | **yes** |
| **corpus day** | `Strader/data/corpus/` | the date | the collectors | written once, repaired | value, not entity? |
| **skill** | `.claude/skills/` | directory name | the repo | none declared | no lifecycle yet |
| **formula / molecule** | `.beads/formulas/` | file name | gc | none declared | no lifecycle yet |
| **desk page** | `/var/moo/desk/` | slug | the producer | overwritten in place | a view, not an entity |
| **service** | — | — | — | — | **undefined, and it is what dr-ok8 waits on** |

The bottom row connects this to work already queued. Your ruling of 2026-09-18
said it plainly: *"every service can expect to be queried by other services,
and that has to be part of what being a service is, built in to its object
model."* That cannot be implemented until **service** has a row in this table.

## 7. The four decisions that unlock everything else

Each is one word from you.

1. **Do Zentity and entity stay separate axes** (ownership vs identity), per §4?
   *Recommended: yes.*
2. **Is OKF's extended header the base for every entity**, not only knowledge
   files? *Recommended: yes — it runs, it is read as data, and the alternative
   is a second standard.*
3. **Is the relation shape `{from, to, kind}`** with a closed vocabulary?
   *Recommended: yes.*
4. **Is the register generated rather than hand-maintained?**
   *Recommended: yes.*

## 8. What a conventional architect does next, in order

1. **Hydrate** — this document, corrected by you. One pass.
2. **Decide** the four above. Nothing else is blocked on anything else.
3. **Sort the inventory** — for each candidate, answer questions 1, 3, 4 or
   move it out of the entity list. This is the bulk of the work and it is
   conversation, not code.
4. **Write the one-page definition** that survives the sort, and put it in COO
   where both other repos can read it.
5. **Map the seams.** Where two repos name the same thing differently, write
   the translation. Never claim the two are the same thing; st-1s1 is the
   standing lesson.
6. *Then* build the visualiser (dr-ok8). It becomes trivial once §5.6 has an
   answer: one relation shape, one renderer.

Steps 1–3 are where your cohesion instinct does the real work. Step 6 is the
part that looked like the request and is actually the consequence.
