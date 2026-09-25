"""The prompts mread.py sends Gemini, and the reply shape it falls back to."""

# The empty-reply shape an ask or transcribe falls back to when Gemini's reply
# is not JSON — the keys the curated tooling reads first.
ASK_SHAPE = {"summary": None, "claims": []}

ANALYST_PROMPT = """You are a video analyst. Answer the question below about the
video, then report your findings as JSON ONLY (no markdown fences, no prose
outside the JSON) with this exact shape:

{
  "summary": "2-4 sentence direct answer to the question",
  "claims": [
    {
      "t": "MM:SS",
      "kind": "onscreen_text | visual | spoken | inferred",
      "claim": "one specific, checkable statement",
      "verbatim": "exact on-screen text if kind is onscreen_text, else null"
    }
  ],
  "uncertainties": ["anything you could not read clearly or are unsure of"]
}

Rules:
- EVERY claim must carry a timestamp of the moment that evidences it.
- Transcribe on-screen text verbatim; never round or paraphrase numbers.
- If text is too small/blurry to read, say so in uncertainties rather than guessing.
- Prefer many small precise claims over few broad ones.

QUESTION: {question}
"""

TRANSCRIBE_PROMPT = """This video is a screen recording of one chapter of a recorded
trading course: a presenter narrates over slides and over chart software
(thinkorswim, Bookmap, footprint charts). Captions may be burned in at the
bottom of the frame; the audio is authoritative and the captions are a cross-check.

Produce JSON ONLY (no fences, no prose outside it) with this exact shape:

{
  "segments": [
    {"t": "MM:SS", "speech": "the presenter's words, verbatim, for the ~10-20 s beginning at t",
     "screen": "slide | chart | mixed | other",
     "note": "what changed on screen at t if anything (new slide title, chart tool, a level drawn, the orange clock label reading), else null"}
  ],
  "slides": [
    {"t": "MM:SS", "title": "slide heading verbatim", "text": "every bullet verbatim, one per line, in the slide's final built-up form"}
  ],
  "uncertainties": ["anything not heard or read clearly"]
}

Rules:
- Timestamps are measured from the START of the video segment you were given.
- Speech is VERBATIM: keep his phrasing, his numbers, his hedges. You may drop
  pure stutters ("we we we") but never summarize, reorder or clean up meaning.
- Cover the whole segment with no gaps: consecutive segments should abut.
- Transcribe numbers exactly as spoken and exactly as written; never round.
- Every distinct slide appears once in "slides", at its first appearance, with
  its complete text. If bullets are revealed progressively, give the final form.
- If something cannot be read or heard, put it in uncertainties rather than guess.
"""
