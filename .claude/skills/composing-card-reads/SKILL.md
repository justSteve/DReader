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

## Before you finish

- Every number in the read appears in `CARD.md`, or is marked unverified.
- Every named cross-reference points at a card that exists.
- No provenance markers, no `kind:` labels, no bare `(mm:ss)` inside L0–L2.
- Read L1 aloud. If it sounds like a database row, rewrite it.
- Do not touch `CARD.md`. If composing surfaces a factual error in the card,
  report it — do not fix it here and let the two drift.
