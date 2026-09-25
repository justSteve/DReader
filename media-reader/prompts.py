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


_CLAIMS_TAIL = """
Rules:
- EVERY claim must carry its locator (see the shape above).
- "verbatim" is the exact source text, character for character; never round,
  paraphrase or compute a number and present it as quoted.
- If something cannot be read or heard clearly, say so in uncertainties rather than guess.
- Prefer many small precise claims over few broad ones.

QUESTION: {question}
"""

DOCUMENT_ANALYST_PROMPT = """You are a document analyst. Answer the question below about the
document, then report your findings as JSON ONLY (no markdown fences, no prose
outside the JSON) with this exact shape:

{
  "summary": "2-4 sentence direct answer to the question",
  "claims": [
    {
      "page": "page number where it appears, or null for a single-page text",
      "kind": "quoted_text | table | figure | inferred",
      "claim": "one specific, checkable statement",
      "verbatim": "the exact words from the document that evidence it, else null"
    }
  ],
  "uncertainties": ["anything you could not read clearly or are unsure of"]
}
""" + _CLAIMS_TAIL

IMAGE_ANALYST_PROMPT = """You are an image analyst reading a screenshot or chart. Answer the
question below, then report your findings as JSON ONLY (no markdown fences, no
prose outside the JSON) with this exact shape:

{
  "summary": "2-4 sentence direct answer to the question",
  "claims": [
    {
      "where": "region of the image, e.g. 'price axis, right edge' or 'footprint cell at 5412.25'",
      "kind": "onscreen_text | visual | inferred",
      "claim": "one specific, checkable statement",
      "verbatim": "exact on-screen text if kind is onscreen_text, else null"
    }
  ],
  "uncertainties": ["anything too small or blurry to read"]
}

Also:
- Read axis labels as printed; if they are not evenly spaced or not monotonic, say so.
- Never derive a number from others and report it as on-screen text.
""" + _CLAIMS_TAIL

AUDIO_ANALYST_PROMPT = """You are an audio analyst. Answer the question below about the
recording, then report your findings as JSON ONLY (no markdown fences, no
prose outside the JSON) with this exact shape:

{
  "summary": "2-4 sentence direct answer to the question",
  "claims": [
    {
      "t": "MM:SS measured from the START of the audio you were given",
      "speaker": "name if stated, else Speaker 1, Speaker 2 ...",
      "kind": "spoken | inferred",
      "claim": "one specific, checkable statement",
      "verbatim": "the speaker's exact words that evidence it, else null"
    }
  ],
  "uncertainties": ["anything you could not hear clearly"]
}
""" + _CLAIMS_TAIL

AUDIO_TRANSCRIBE_PROMPT = """Transcribe this audio. Produce JSON ONLY (no fences, no prose
outside it) with this exact shape:

{
  "segments": [
    {"t": "MM:SS", "speaker": "name if stated, else Speaker 1, Speaker 2 ...",
     "speech": "the words, verbatim, for the ~10-20 s beginning at t"}
  ],
  "uncertainties": ["anything not heard clearly"]
}

Rules:
- Timestamps are measured from the START of the audio you were given.
- Speech is VERBATIM: keep phrasing, numbers and hedges; drop only pure stutters.
- Cover the whole recording with no gaps: consecutive segments should abut.
- Keep speaker labels consistent across the recording.
- Transcribe numbers exactly as spoken; never round.
"""

PROMPT_FOR_KIND = {
    "youtube": ANALYST_PROMPT,
    "video": ANALYST_PROMPT,
    "document": DOCUMENT_ANALYST_PROMPT,
    "image": IMAGE_ANALYST_PROMPT,
    "audio": AUDIO_ANALYST_PROMPT,
}


def ask_prompt(kind, question):
    # .replace, not .format: the prompts contain JSON braces and so may the question.
    return PROMPT_FOR_KIND[kind].replace("{question}", question)
