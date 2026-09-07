---
name: composing-card-reads
description: Use when writing or revising a human-facing READ.md for a yt-analyst video card — composing the presenter's transcript into a four-level progressive read with editorial cross-links
---

# Composing Card Reads

## Overview

`videos/<id>/CARD.md` is written for machines and for future analysts: dense,
timestamped, provenance-marked, deliberately compressed. It is the record of
truth and it stays exactly as it is.

`videos/<id>/READ.md` is the human version. It is composed **from the
transcript**, not from the card, because the card is a lossy compression that
already discarded the presenter's voice, examples and explanations. You cannot
decompress good reading out of it.

The card says: *"A setup is defined at 04:41 as a price, volume or footprint
formation that reduces risk."*
The transcript says: *"A setup is nothing more than a formation of price or
volume or a footprint or whatever that gives me an advantage in keeping my risk
smaller."*

The second is the one a person wants to read. Your job is to keep that voice
and put an editor around it.

**Announce at start:** "I'm using the composing-card-reads skill."

## Inputs

| File | Role |
|---|---|
| `videos/<id>/transcript.txt` | **The substrate.** The presenter's own words. |
| `videos/<id>/CARD.md` | Fact-check and provenance. Timestamps, verbatim on-screen text, verified numbers. |
| `playlists/*.md` | The corpus. Where this video agrees, conflicts, or fills a gap. |
| `corpus.json` | Cross-reference edges — which cards already link here. |

**The card wins on facts.** Where transcript and card disagree on a number, a
name or an on-screen string, the card is right — it was checked against the
video and often against arithmetic. Where they disagree on *wording*, the
transcript is right.

## The four levels

Write all four, in this order, in one file. The UI reveals them progressively.

**L0 — one line.** What this video is. No hedging, no "this video discusses".
Name the thing it actually contributes.

**L1 — the overview.** ~150 words. What the presenter is arguing and why it
matters to us. A reader who stops here should be able to hold their own in a
conversation about it.

**L2 — the argument.** 400–800 words. How the reasoning actually goes, in
order. This is where corpus connections live: where he agrees with another
source, where he conflicts, what gap he fills. Cross-links are **inline and
named** — say *who* he agrees with and *about what*, never "see also".

**L3 — the edited transcript.** The presenter teaching, in his own words,
trimmed to the priority material. Editorial notes sit alongside as blockquoted
asides, clearly marked as ours. Length follows the source; a dense 30-minute
video earns more than a thin 9-minute one.

## What survives the cut (the priority lens)

Keep:

1. **Order-flow reasoning** — how he thinks about volume, absorption, auction
   and trade location. The reasoning, not just the conclusion.
2. **Cross-source connections** — any passage that agrees with, conflicts with,
   or fills a gap in another source in the corpus. These are the spine.
3. **Teaching quality** — passages where he explains something well, even when
   the content is not novel to us. Good explanation is the point of a read.

Cut without mercy:

- Sales, upsell, discount codes, QR-code banners, community pitches
- Channel intros, outros, subscribe prompts, sponsor reads
- Anecdote that carries no method
- Repetition — presenters restate constantly; keep the best statement once
- Segments off the order-flow axis entirely

## Voice

- **Write for a reader, not a grader.** No `**Verified: arithmetic**`, no
  `(kind: onscreen_text)`, no provenance markers in the prose.
- **Timestamps go in the margin, not mid-sentence.** L3 passages carry a
  timestamp anchor; L0–L2 prose does not interrupt itself with `(04:41)`.
- **Quote the presenter; paraphrase yourself.** When his sentence is better
  than yours, use his and attribute it.
- **One idea per paragraph.** The card packs four; a read does not.
- **Editorial voice is distinct and honest.** When we think he is wrong,
  unsupported or overselling, say so plainly in an aside — do not launder it
  into neutral summary and do not moralise about it.
- No em-dash pileups, no bolded phrase every other line. The card does that
  because it is scanned; a read is read.

## Handling the transcript's known defects

Auto-captions fail in two predictable ways. **Fix silently only where the card
proves the correct value; otherwise flag.**

- **Native-English uploads** come back unpunctuated and lowercase. Restore
  sentences and capitals. This is transcription repair, not editing — do not
  change word choice while you do it.
- **AI-dubbed uploads** (this corpus: the German channel) are punctuated but
  mangle proper nouns: `PVD` for PbD, `Forwald` for Vorwald, `Nelles` for Nill,
  `Rydeczka` for Radecker. Correct these against the card, silently.
- **Never invent a number from a transcript.** Captions mis-hear digits. If a
  figure is not in the card, either omit it or mark it as unverified.
- **Do not smooth away a hedge.** If he says "roughly" or "I think", keep it.

## Output shape

```markdown
# Read: <Title>

> **<L0 — one line>**

- **Channel:** … · **Uploaded:** … · **Duration:** …
- **Card:** [CARD.md](CARD.md) · **Watch:** <url>

## In brief
<L1 — ~150 words>

## The argument
<L2 — 400–800 words, corpus connections inline and named>

## In his words
<L3 — edited transcript with timestamp anchors and editorial asides>
```

Editorial asides inside L3 use a marked blockquote so the UI can style them
apart from the presenter's voice:

```markdown
> **Editor —** Carmine's series never states a win rate anywhere in eight
> episodes. This is the slide that closes that gap.
```

## The card audit (a required deliverable, not a side note)

Composing from the transcript **audits the card**, and on the first video it
tried this it found a wrong number that had already propagated into two other
files. Treat the audit as half the job.

As you compose, check every figure, name and quoted string in `CARD.md` against
what the transcript actually says. Report — do not fix — anything in these
classes:

1. **A hedge hardened into an assertion.** "maybe a two" recorded as
   "greater than 2"; "if you should reach 50%" recorded as a "planning hit
   rate". This is the most common and most damaging class.
2. **A paraphrase tabulated as a quote.** Check the run JSON under
   `videos/<id>/runs/*/response.json`: a claim with **`verbatim: null`** is
   Gemini's paraphrase, not anyone's words. It must never appear in a card's
   numbers table as a stated value.
3. **A spoken claim attributed to the screen.** Check `kind`. `kind: spoken` is
   not on-screen text however slide-like it reads.
4. **A number the transcript contradicts**, or that appears nowhere in it.
5. **A name or term the card gets wrong** — noting that captions mangle proper
   nouns, so the card is usually right and the caption wrong. Flag only when
   the transcript is clearly the better source.

Report each finding as: the card's text, the transcript's actual words with
their timestamp, and which class above it falls into. If you find nothing,
say so explicitly — a clean audit is a result.

**Never edit `CARD.md` yourself.** Corrections are reconciled centrally, because
a hardened figure usually appears in more than one file and fixing one copy
creates a silent inconsistency.

## Before you finish

- Every number in the read appears in `CARD.md`, or is marked unverified.
- Every named cross-reference points at a card that exists.
- No provenance markers, no `kind:` labels, no bare `(mm:ss)` inside L0–L2.
- Read L1 aloud. If it sounds like a database row, rewrite it.
- Do not touch `CARD.md`. If composing surfaces a factual error in the card,
  report it — do not fix it here and let the two drift.

## Scope: SPX/ES only

The reads serve a trader of the S&P. Detail on any other instrument is cut,
including passages that make a general order-flow point on a DAX, gold, bond
or Euro Stoxx example; elide inside quotations with `[...]`, retitle the
passage if its title named the instrument, and rewrite L0–L2 so no cut figure
survives there. Log each cut in `yt-analyst/EDITS.md`. `CARD.md` keeps the
full record; only `READ.md` is scoped.
