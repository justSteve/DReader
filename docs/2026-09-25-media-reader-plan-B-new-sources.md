# media-reader, Plan B — documents, images, audio

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `mread.py` ingests and interrogates three new source kinds: **documents** (PDF, text, email, HTML), **images** (screenshots, charts) and **audio** (podcasts, recordings). Each comes with a verification command that fits its medium, the way `frames` fits video.

**Bead:** dr-dqm.2 (under epic dr-dqm). **Prerequisite:** Plan A (dr-dqm.1) closed. This plan uses its `Source`, `KIND_BY_EXT`, `media_part`, `dossier_dir` and `dreader_core`.

**Architecture:** Each kind is a row in `KIND_BY_EXT`, a prompt in `PROMPT_FOR_KIND`, a branch in `media_part`, and one verification command. Documents and images go to Gemini inline (text Part or image bytes) unless they are large. PDFs and audio go through the Files API upload cache. Audio windows are cut **locally** with ffmpeg: the server-side `VideoMetadata` offsets apply to video only. A `source.json` in each dossier remembers the local file, so later commands need only `--id`.

**Tech Stack:** as Plan A, plus poppler-utils (`pdftotext`, `pdftoppm`; installed at `/usr/bin`), Python `email` and `html.parser` (stdlib).

---

## Verification doctrine per kind (the reason each command exists)

The yt-analyst doctrine is *wide pass → zoom → check arithmetic → verify against pixels*, and **arithmetic verifies consistency, not provenance** (Cherry Bomb, LESSONS.md). Each new kind needs its own answer to "what is the independent check?":

| Kind | Zoom | Independent check | Command |
|---|---|---|---|
| document | ask about a page range | **every `verbatim` quote must appear in the source text**. The check is mechanical, costs nothing, and catches a derived number presented as quoted | `verify-quotes`; `pages` renders page images for tables and figures |
| image | `ask --crop x,y,w,h` | Claude views the image itself. There is no second sample, so this is the only check (Strader, 2026-08-30). Apply the zero-cost filters first: footprint parity, too-neat numbers, non-monotonic axis | `crop` output is readable with the Read tool |
| audio | `ask --start --end` on a local cut | no pixels. A load-bearing spoken number needs a **second, separately cut** pass over ±15 s that agrees verbatim. Disagreement goes to Steve with both versions | `ask` twice on offset windows |

Task B5 writes this into `media-reader/CLAUDE.md`.

## Hazards

- Same card freeze and oracle as Plan A. Take a fresh `compare_outputs.py save` before Task B1. Tasks B1–B4 must leave the existing corpus's outputs **identical**; only B5 changes them, on purpose.
- Source files can be private (newsletters, members-only audio). `dossiers/*/source.*`, `source.json`, `chunks/`, `crops/` and `pages-*/` are gitignored in Task B1, before any specimen exists.
- `uploads.upload_file` calls `sys.exit` on a FAILED upload, which `except Exception` does not catch. In `transcribe_audio`, one failed chunk upload therefore ends the whole run. That is acceptable, because the finished chunks are archived under `runs/`, but say so in the B4 LESSONS entry if it happens (Task 4 review).
- Gemini inline requests are capped near 20 MB. `INLINE_MAX` is 18 MB; anything larger goes through the upload cache.

## File map

| Path | Status | Responsibility |
|---|---|---|
| `media-reader/documents.py` | create | text extraction (PDF, email, HTML, plain), quote normalisation and checking |
| `media-reader/cuts.py` | create | local ffmpeg cuts: audio windows, image crops; ffprobe for image size |
| `media-reader/prompts.py` | modify | per-kind analyst prompts, audio transcription prompt, `ask_prompt()` |
| `media-reader/sources.py` | modify | new kinds, the generic media card, `source.json`, id-only resolution, `media_part` branches |
| `media-reader/perceive.py` | modify | `ask` per kind (crop, audio cut, re-basing), `transcribe` for audio, `fetch` |
| `media-reader/verify.py` | modify | `pages`, `verify-quotes`; `frames` refuses non-video |
| `media-reader/corpus.py` | modify | kind tag in INDEX, export verification vocabulary |
| `media-reader/mread.py` | modify | subcommands and flags |
| `media-reader/.gitignore` | modify | private source copies and working cuts |
| `tests/media_reader/test_documents.py`, `test_cuts.py`, `test_kinds.py`, `test_prompts.py` | create | unit tests |

---

### Task B1: Kinds, the generic card, `source.json`, id-only resolution

**Files:** `media-reader/sources.py`, `media-reader/.gitignore`, `tests/media_reader/test_kinds.py`

- [ ] **Step 1: Gitignore first**

Append to `media-reader/.gitignore`:
```
# dr-dqm.2 — private source copies, machine-local pointers, working cuts
dossiers/*/source.*
dossiers/*/chunks/
dossiers/*/crops/
dossiers/*/pages-*/
dossiers/*/*.upload.json
```
Check that nothing already tracked matches, since that would mean hiding committed files: `git ls-files media-reader/dossiers | /usr/bin/grep -E '/source\.|/chunks/|/crops/|/pages-'`. Expected: no output.

- [ ] **Step 2: Write the failing tests**

Create `tests/media_reader/test_kinds.py`:
```python
import argparse

import pytest

import sources


@pytest.fixture(autouse=True)
def tmp_dossiers(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")


def ns(**kw):
    base = {"url": None, "file": None, "id": None}
    base.update(kw)
    return argparse.Namespace(**base)


def make(tmp_path, name, data=b"x"):
    f = tmp_path / name
    f.write_bytes(data)
    return f


@pytest.mark.parametrize("name,kind,mime", [
    ("a.pdf", "document", "application/pdf"),
    ("a.txt", "document", "text/plain"),
    ("a.md", "document", "text/markdown"),
    ("a.eml", "document", "message/rfc822"),
    ("a.html", "document", "text/html"),
    ("a.png", "image", "image/png"),
    ("a.JPG", "image", "image/jpeg"),
    ("a.webp", "image", "image/webp"),
    ("a.mp3", "audio", "audio/mpeg"),
    ("a.m4a", "audio", "audio/mp4"),
    ("a.wav", "audio", "audio/wav"),
    ("a.mp4", "video", "video/mp4"),
])
def test_kind_by_extension(tmp_path, name, kind, mime):
    s = sources.resolve_source(ns(file=str(make(tmp_path, name)), id="spec-item"))
    assert (s.kind, s.mime) == (kind, mime)


def test_non_video_kinds_get_the_media_card(tmp_path):
    s = sources.resolve_source(ns(file=str(make(tmp_path, "letter.txt", b"hello")),
                                  id="tb-letter-test"))
    text = s.card.read_text()
    assert text.startswith("# Media: tb-letter-test\n")
    assert "- **Kind:** document" in text and "letter.txt" in text
    assert "## Findings" in text and text.rstrip().endswith(
        "_(machine-appended by mread.py — do not edit above this line's entries)_")


def test_id_alone_finds_the_remembered_file(tmp_path):
    f = make(tmp_path, "chart.png")
    first = sources.resolve_source(ns(file=str(f), id="chart-one"))
    again = sources.resolve_source(ns(id="chart-one"))
    assert (again.kind, again.path, again.card) == (first.kind, first.path, first.card)


def test_id_alone_without_a_dossier_says_so():
    with pytest.raises(SystemExit, match="no remembered source"):
        sources.resolve_source(ns(id="never-seen"))


def test_origin_is_recorded_on_the_card(tmp_path):
    f = make(tmp_path, "ep.m4a")
    s = sources.resolve_source(ns(file=str(f), id="pod-ep-1",
                                  origin="https://example.com/ep1"))
    assert "https://example.com/ep1" in s.card.read_text()
```

- [ ] **Step 3: Run and watch them fail**

Run: `.venv/bin/pytest tests/media_reader/test_kinds.py -q`
Expected: the parametrized non-video cases fail with `SystemExit: --file: unsupported type .pdf …`, and the card, id-only and origin tests fail.

- [ ] **Step 4: Implement**

In `sources.py`, extend `KIND_BY_EXT`:
```python
KIND_BY_EXT.update({
    ".pdf": ("document", "application/pdf"),
    ".txt": ("document", "text/plain"),
    ".md": ("document", "text/markdown"),
    ".eml": ("document", "message/rfc822"),
    ".html": ("document", "text/html"),
    ".htm": ("document", "text/html"),
    ".png": ("image", "image/png"),
    ".jpg": ("image", "image/jpeg"),
    ".jpeg": ("image", "image/jpeg"),
    ".webp": ("image", "image/webp"),
    ".mp3": ("audio", "audio/mpeg"),
    ".m4a": ("audio", "audio/mp4"),
    ".wav": ("audio", "audio/wav"),
    ".ogg": ("audio", "audio/ogg"),
    ".opus": ("audio", "audio/ogg"),
    ".flac": ("audio", "audio/flac"),
    ".aac": ("audio", "audio/aac"),
})
```
Add the generic card:
```python
CARD_TEMPLATE_MEDIA = """# Media: {id}

- **Kind:** {kind}
- **Source:** {source}
- **First analyzed:** {date}
- **Status:** open

## Findings
_(curated by Claude Code: verified findings, each with its locator — timestamp, page or image region)_

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

## Lessons (this item)
_(anything peculiar to this source: layout, speakers, document structure)_

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
"""


def describe(path, kind):
    """The card's Source line: where the file is and the one size that matters."""
    mb = path.stat().st_size / 1e6
    if kind == "audio":
        secs = probe_duration(path)
        extent = f"{fmt_ts(secs)} ({secs} s)" if secs else "duration unknown"
    elif kind == "image":
        from cuts import image_size
        w, h = image_size(path)
        extent = f"{w}×{h}" if w else "size unknown"
    elif kind == "document":
        from documents import page_count
        extent = f"{page_count(path)} page(s)"
    else:
        extent = ""
    return f"local `{path}` ({mb:.1f} MB{', ' + extent if extent else ''})"
```
(`cuts.image_size` and `documents.page_count` arrive in Tasks B2 and B3. Until then, create both modules with just these two functions so the tests run:)

`media-reader/cuts.py` (initial):
```python
"""Local ffmpeg cuts: the zoom step for kinds Gemini cannot window itself."""
import subprocess


def image_size(path):
    """(width, height) via ffprobe; (0, 0) if it cannot tell."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        w, h = out.split(",")[:2]
        return int(w), int(h)
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return 0, 0
```
`media-reader/documents.py` (initial):
```python
"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import subprocess


def pdf_text(path):
    """pdftotext -layout; pages end in \\f. Empty string if poppler fails."""
    try:
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def page_count(path):
    if path.suffix.lower() != ".pdf":
        return 1
    return max(1, pdf_text(path).count("\f"))
```
Rewrite `resolve_source`'s file branch so it handles id-only lookup, `source.json` and the card choice. The whole function after this step:
```python
def _remembered(vid):
    rec = DOSSIERS_DIR / vid / "source.json"
    if not rec.exists():
        sys.exit(f"--id {vid}: no remembered source in {rec.parent}/ — "
                 "give --file (or --url) the first time")
    return json.loads(rec.read_text())


def resolve_source(args):
    """The Source named by --url, --file/--id, or --id alone (a dossier that
    remembers its file). Creates the card on first contact; never rewrites one."""
    path = getattr(args, "file", None)
    url = getattr(args, "url", None)
    vid = getattr(args, "id", None)
    origin = getattr(args, "origin", None)
    if not path and not url and vid:
        rec = _remembered(vid)
        path, origin = rec["path"], origin or rec.get("origin")
    if path:
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            sys.exit(f"--file: not a file: {path}")
        kind, mime = kind_for(path)
        if not vid or not LOCAL_ID_RE.match(vid):
            sys.exit("--file needs --id: a slug like it-orderflow-absorption-4142 "
                     "(lowercase letters, digits, hyphens; it names dossiers/<id>/)")
        if extract_video_id(vid + "x") and len(vid) == 11:
            sys.exit(f"--id {vid} looks like a YouTube id; pick a slug")
        d = dossier_dir(vid)
        (d / "source.json").write_text(json.dumps(
            {"path": str(path), "origin": origin}, indent=2))
        card = d / "CARD.md"
        if not card.exists():
            today = datetime.now().strftime("%Y-%m-%d")
            if kind == "video":
                secs = probe_duration(path)
                card.write_text(CARD_TEMPLATE_LOCAL.format(
                    video_id=vid, kind=kind, path=path,
                    size_mb=path.stat().st_size / 1e6,
                    duration=f"{fmt_ts(secs)} ({secs} s)" if secs else "duration unknown",
                    date=today))
            else:
                src_line = describe(path, kind)
                if origin:
                    src_line = f"{origin} → {src_line}"
                card.write_text(CARD_TEMPLATE_MEDIA.format(
                    id=vid, kind=kind, source=src_line, date=today))
        return Source(kind=kind, id=vid, card=card, path=path, mime=mime)
    if not url:
        sys.exit("give --url (YouTube), --file PATH --id ID (local file), "
                 "or --id ID (a dossier that remembers its file)")
    vid = extract_video_id(url)
    if not vid:
        sys.exit(f"Could not extract a YouTube video id from: {url}")
    url = canonical_url(vid)
    return Source(kind="youtube", id=vid, card=ensure_card(vid, url), url=url)
```
Add `import json` to `sources.py`. `source.json` is gitignored (Step 1). It holds a machine-local path, like `upload.json`.

- [ ] **Step 5: Run the tests**

Run: `.venv/bin/pytest tests -q`
Expected: all pass, including Plan A's `test_sources.py`.

- [ ] **Step 6: Oracle and commit**

```bash
.venv/bin/python tests/media_reader/compare_outputs.py check
git add media-reader tests
git commit -m "[dr-dqm.2] Document, image and audio kinds; generic media card; dossiers remember their file"
```
Expected: four `identical`. Existing cards and dossiers are untouched. A `source.json` appears only when a `--file` command runs.

---

### Task B2: Documents — extraction, prompt, `verify-quotes`, `pages`

**Files:** `media-reader/documents.py`, `prompts.py`, `sources.py` (`media_part`), `perceive.py` (`cmd_ask`), `verify.py`, `mread.py`; tests `test_documents.py`, `test_prompts.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/media_reader/test_documents.py`:
```python
import documents

EML = b"""From: Matt <newsletter@tradebrigade.co>
To: steve@example.com
Date: Sun, 31 Aug 2026 18:02:00 -0400
Subject: Trade Brigade - Week Ahead
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="b"

--b
Content-Type: text/plain; charset="utf-8"

SPY closed at 645.31. Watch 640 as support.
--b
Content-Type: text/html; charset="utf-8"

<p>SPY closed at <b>645.31</b>.</p>
--b--
"""


def test_email_prefers_the_plain_part_and_keeps_headers(tmp_path):
    p = tmp_path / "l.eml"
    p.write_bytes(EML)
    t = documents.extract_text(p)
    assert "Subject: Trade Brigade - Week Ahead" in t
    assert "SPY closed at 645.31. Watch 640 as support." in t
    assert "<b>" not in t


def test_html_drops_tags_scripts_and_styles(tmp_path):
    p = tmp_path / "a.html"
    p.write_text("<style>x{}</style><h1>Title</h1><p>One &amp; two</p>"
                 "<script>alert(1)</script><p>three</p>")
    t = documents.extract_text(p)
    assert "Title" in t and "One & two" in t and "three" in t
    assert "alert" not in t and "x{}" not in t


def test_quote_normalisation_forgives_typography_not_digits():
    text = "He said “buy above 311” — then  waited."
    assert documents.quote_found('He said "buy above 311" - then waited.', text)
    assert not documents.quote_found('He said "buy above 312"', text)


def test_check_quotes_reports_each_claim():
    claims = [{"verbatim": "Watch 640 as support"}, {"verbatim": "Watch 650"},
              {"verbatim": None}, {"claim": "no verbatim key"}]
    rows = documents.check_quotes(claims, "SPY closed at 645.31. Watch 640 as support.")
    assert [r[1] for r in rows] == [True, False]
```
Create `tests/media_reader/test_prompts.py`:
```python
import pytest

import prompts


@pytest.mark.parametrize("kind,marker", [
    ("youtube", '"t": "MM:SS"'), ("video", '"t": "MM:SS"'),
    ("audio", '"speaker"'), ("image", '"where"'), ("document", '"page"'),
])
def test_each_kind_has_its_locator(kind, marker):
    p = prompts.ask_prompt(kind, "What is the level?")
    assert marker in p and p.rstrip().endswith("QUESTION: What is the level?")


def test_question_braces_do_not_break_formatting():
    assert "{x}" in prompts.ask_prompt("document", "what is {x}?")
```

- [ ] **Step 2: Run and watch them fail**

Run: `.venv/bin/pytest tests/media_reader/test_documents.py tests/media_reader/test_prompts.py -q`
Expected: `AttributeError: module 'documents' has no attribute 'extract_text'` and `… 'prompts' has no attribute 'ask_prompt'`.

- [ ] **Step 3: Implement `documents.py`**

Add to `media-reader/documents.py`:
```python
import email
import re
from email import policy
from html.parser import HTMLParser


class _Text(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)


def html_to_text(html):
    p = _Text()
    p.feed(html)
    return re.sub(r"\n{3,}", "\n\n", "".join(p.out)).strip() + "\n"


def email_text(path):
    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    head = "\n".join(f"{h}: {msg[h]}" for h in ("From", "To", "Date", "Subject") if msg[h])
    body = msg.get_body(preferencelist=("plain", "html"))
    text = body.get_content() if body else ""
    if body is not None and body.get_content_type() == "text/html":
        text = html_to_text(text)
    return f"{head}\n\n{text}"


def extract_text(path):
    """The document's text as Gemini's claims will be checked against it."""
    suf = path.suffix.lower()
    if suf == ".pdf":
        return pdf_text(path)
    if suf == ".eml":
        return email_text(path)
    if suf in (".html", ".htm"):
        return html_to_text(path.read_text(errors="replace"))
    return path.read_text(errors="replace")


_TYPO = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'",
                       "—": "-", "–": "-", " ": " "})


def normalise(s):
    """Forgive typography and whitespace; never digits, words or case."""
    return re.sub(r"\s+", " ", s.translate(_TYPO)).strip()


def quote_found(quote, text):
    return normalise(quote) in normalise(text)


def check_quotes(claims, text):
    """[(claim, found)] for every claim that carries a verbatim quote."""
    return [(c, quote_found(c["verbatim"], text))
            for c in claims if c.get("verbatim")]
```

- [ ] **Step 4: Implement per-kind prompts**

Add to `media-reader/prompts.py`:
```python
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
```

- [ ] **Step 5: Run the unit tests**

Run: `.venv/bin/pytest tests/media_reader -q`
Expected: all pass.

- [ ] **Step 6: Route documents through `media_part` and `ask`**

In `sources.py`, replace `media_part` with the kind-aware version (Task B3 adds the image branch into the same function):
```python
INLINE_MAX = 18_000_000  # Gemini inline requests cap near 20 MB
TEXT_MIMES = {"text/plain", "text/markdown", "message/rfc822", "text/html"}


def media_part(client, src, vm_kwargs=None, path=None, mime=None):
    """The Part that carries src's bytes to Gemini. `path`/`mime` substitute a
    local cut (an audio chunk, an image crop) for the whole source."""
    from google.genai import types
    path, mime = path or src.path, mime or src.mime
    if src.kind == "youtube":
        return types.Part(file_data=types.FileData(file_uri=src.url),
                          video_metadata=types.VideoMetadata(**vm_kwargs) if vm_kwargs else None)
    if src.kind == "document" and mime in TEXT_MIMES:
        from documents import extract_text
        return types.Part.from_text(text=extract_text(path))
    cache = (dossier_dir(src.id) / "upload.json" if path == src.path
             else path.with_name(path.name + ".upload.json"))
    g = uploads.upload_cached(client, cache, path, mime)
    return types.Part(
        file_data=types.FileData(file_uri=g.uri, mime_type=g.mime_type),
        video_metadata=(types.VideoMetadata(**vm_kwargs)
                        if vm_kwargs and src.kind == "video" else None),
    )
```
In `perceive.cmd_ask`:
- `prompt = ANALYST_PROMPT.replace("{question}", args.question)` → `prompt = ask_prompt(src.kind, args.question)`
- directly after `src = resolve_source(args)`:
  ```python
      if src.kind in ("document", "image") and (args.start or args.end or args.fps):
          sys.exit(f"ask: --start/--end/--fps do not apply to a {src.kind}; "
                   "ask about a page range in the question, or --crop an image")
  ```
- `vm_kwargs` is built only when `src.kind in ("youtube", "video")`, so wrap the existing three `if args.…` lines in that condition.

- [ ] **Step 7: `verify-quotes` and `pages`**

Add to `media-reader/verify.py`:
```python
import json

from documents import check_quotes, extract_text


def latest_run(dossier, ts=None):
    runs_dir = dossier / "runs"
    if ts:
        return runs_dir / ts
    # Run dirs are <date>-<time>[-n]; sort numerically on the collision
    # suffix so -10 follows -2 (plain name order would not) [Task 4 review].
    def order(d):
        parts = d.name.split("-")
        return (parts[0], parts[1], int(parts[2]) if len(parts) > 2 else 1)
    dirs = sorted((d for d in runs_dir.iterdir() if (d / "response.json").exists()),
                  key=order)
    if not dirs:
        sys.exit(f"no runs with a response.json under {runs_dir}/")
    return dirs[-1]


def cmd_verify_quotes(args):
    """Every verbatim quote in a run's claims must appear in the source text.
    Exit 1 if any is missing — a missing quote is a finding, not a formatting nit."""
    src = resolve_source(args)
    if src.kind != "document":
        sys.exit(f"verify-quotes: {src.kind} sources have no text layer to check against")
    run = latest_run(dossier_dir(src.id), args.run)
    claims = json.loads((run / "response.json").read_text()).get("claims") or []
    text = extract_text(src.path)
    if not text.strip():
        sys.exit(f"verify-quotes: no extractable text in {src.path.name} "
                 "(scanned PDF?) — use `pages` and read the page images")
    rows = check_quotes(claims, text)
    for c, ok in rows:
        loc = f"p.{c['page']}" if c.get("page") else "   "
        print(f"{'OK     ' if ok else 'MISSING'} {loc:>5}  {c['verbatim'][:90]}")
    missing = sum(1 for _, ok in rows if not ok)
    print(f"\n{len(rows)} quoted claims in {run.name}: {len(rows) - missing} found, "
          f"{missing} missing; {len(claims) - len(rows)} claims carry no quote")
    sys.exit(1 if missing else 0)


def cmd_pages(args):
    """Render PDF pages to PNG (and their text layer) for Claude to read."""
    src = resolve_source(args)
    if src.kind != "document" or src.path.suffix.lower() != ".pdf":
        sys.exit("pages: works on PDF documents")
    out = dossier_dir(src.id) / f"pages-{args.first}-{args.last}"
    out.mkdir(parents=True, exist_ok=True)
    rng = ["-f", str(args.first), "-l", str(args.last)]
    subprocess.run(["pdftoppm", *rng, "-r", str(args.dpi), "-png", str(src.path),
                    str(out / "p")], check=True)
    subprocess.run(["pdftotext", *rng, "-layout", str(src.path), str(out / "text.txt")],
                   check=True)
    print(f"{len(list(out.glob('p-*.png')))} page image(s) + text.txt in {out}/")
```
Change `verify.py`'s import from `sources` to `from sources import resolve_source, dossier_dir`.

In `mread.py`, import `cmd_verify_quotes, cmd_pages` from `verify` and register them, next to `frames`:
```python
    q = sub.add_parser("verify-quotes", help="check a run's quoted claims against the document text")
    source_args(q)
    q.add_argument("--run", help="run timestamp (default: newest)")
    q.set_defaults(func=cmd_verify_quotes)

    pg = sub.add_parser("pages", help="render PDF pages + text layer for verification")
    source_args(pg)
    pg.add_argument("--first", type=int, required=True)
    pg.add_argument("--last", type=int, required=True)
    pg.add_argument("--dpi", type=int, default=150)
    pg.set_defaults(func=cmd_pages)
```
In `source_args`, update the help strings to `--file`: *"local file: video, audio, image or document"*, and `--id`: *"dossier id (slug); alone, reuses the file the dossier remembers"*.

- [ ] **Step 8: Real specimen — one Trade Brigade letter**

The letters are already graded by hand in `SCORECARD.md`, so a wrong quote will be visible.
```bash
cd media-reader
L=$(ls newsletters/tradebrigade/letters/*.txt | tail -1); echo "$L"
.venv/bin/python mread.py ask --file "$L" --id tb-letter-smoke \
  --question "Which SPY levels does the letter name, and what does it say about each? Quote it."
.venv/bin/python mread.py verify-quotes --id tb-letter-smoke; echo "exit=$?"
cd ..
```
Expected: a JSON answer whose claims carry `page: null` and verbatim quotes; `verify-quotes` prints one `OK`/`MISSING` row per quote and exits 0 when all are found. **A `MISSING` row is the command working, not failing.** Record any such quote, verbatim, in the Task B5 LESSONS entry.

- [ ] **Step 9: Full tests, oracle, commit**

```bash
.venv/bin/pytest tests -q && .venv/bin/python tests/media_reader/compare_outputs.py check
git add media-reader tests
git commit -m "[dr-dqm.2] Documents: PDF/text/email/HTML ingestion, per-kind prompts, verify-quotes and pages"
```
The oracle may report `INDEX.md: DIFFERS` only because `tb-letter-smoke` now exists as a dossier. Keep that dossier for B6, and check that the only differing rows name it.

---

### Task B3: Images — inline bytes, `--crop`

**Files:** `media-reader/cuts.py`, `sources.py` (`media_part`), `perceive.py`, `mread.py`; test `test_cuts.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/media_reader/test_cuts.py`:
```python
import subprocess

import pytest

import cuts


def test_parse_box():
    assert cuts.parse_box("10,20,300,200") == (10, 20, 300, 200)


@pytest.mark.parametrize("bad", ["10,20,300", "a,b,c,d", "10,20,0,200", "-1,0,10,10"])
def test_parse_box_rejects(bad):
    with pytest.raises(SystemExit, match="--crop"):
        cuts.parse_box(bad)


def test_crop_command_and_output_name(tmp_path):
    cmd, out = cuts.crop_command(tmp_path / "shot.png", (10, 20, 300, 200), tmp_path / "crops")
    assert out == tmp_path / "crops" / "crop-10-20-300x200.png"
    assert cmd[cmd.index("-vf") + 1] == "crop=300:200:10:20"


def test_audio_cut_command_uses_a_duration_not_an_end(tmp_path):
    cmd, out = cuts.audio_cut_command(tmp_path / "ep.m4a", 90, 150, tmp_path / "chunks")
    assert out == tmp_path / "chunks" / "chunk-90-150.m4a"
    assert cmd[cmd.index("-ss") + 1] == "90" and cmd[cmd.index("-t") + 1] == "60"
    assert cmd.index("-ss") < cmd.index("-i")


def test_crop_really_crops(tmp_path):
    src = tmp_path / "shot.png"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=640x480",
                    "-frames:v", "1", str(src)], check=True)
    out = cuts.crop(src, (10, 20, 300, 200), tmp_path / "crops")
    assert cuts.image_size(out) == (300, 200)
```

- [ ] **Step 2: Run and watch them fail**

Run: `.venv/bin/pytest tests/media_reader/test_cuts.py -q`
Expected: `AttributeError: module 'cuts' has no attribute 'parse_box'`.

- [ ] **Step 3: Implement**

Add to `media-reader/cuts.py`:
```python
import re
import sys


def parse_box(s):
    m = re.fullmatch(r"\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*", s or "")
    if not m or int(m.group(3)) == 0 or int(m.group(4)) == 0:
        sys.exit(f"--crop wants X,Y,W,H in pixels (W and H > 0), got {s!r}")
    return tuple(int(g) for g in m.groups())


def crop_command(src, box, out_dir):
    x, y, w, h = box
    out = out_dir / f"crop-{x}-{y}-{w}x{h}.png"
    return ["ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-vf", f"crop={w}:{h}:{x}:{y}", "-frames:v", "1", str(out)], out


def crop(src, box, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = crop_command(src, box, out_dir)
    subprocess.run(cmd, check=True)
    return out


def audio_cut_command(src, a, b, out_dir):
    # -ss and -t as INPUT options: seek, then read b-a seconds. A stream copy
    # needs no re-encode; the cut lands on the nearest frame (tens of ms).
    out = out_dir / f"chunk-{a}-{b}{src.suffix.lower()}"
    return ["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-t", str(b - a),
            "-i", str(src), "-c", "copy", str(out)], out


def cut_audio(src, a, b, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = audio_cut_command(src, a, b, out_dir)
    if not out.exists():
        subprocess.run(cmd, check=True)
    return out
```
In `sources.media_part`, add the image branch right after the text-document branch:
```python
    if src.kind == "image" and path.stat().st_size <= INLINE_MAX:
        return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime)
```
In `perceive.cmd_ask`, after the kind check from B2:
```python
    cut, cut_mime, crop_box = None, None, None
    if getattr(args, "crop", None):
        if src.kind != "image":
            sys.exit("ask: --crop applies to images")
        crop_box = cuts.parse_box(args.crop)
        cut, cut_mime = cuts.crop(src.path, crop_box, dossier_dir(src.id) / "crops"), "image/png"
```
Pass `path=cut, mime=cut_mime` to `media_part(…)`, and add `"crop": args.crop if crop_box else None` to `request.json`. Add `import cuts` and `dossier_dir` to `perceive.py`'s imports. In `mread.py`, on the `ask` parser:
```python
    a.add_argument("--crop", help="images: X,Y,W,H pixel box to zoom on (sent instead of the whole image)")
```
Add a `crop` subcommand too, so Claude can look at a crop without spending a Gemini call:
```python
    c = sub.add_parser("crop", help="images: cut a zoom box to dossiers/<id>/crops/ for viewing")
    source_args(c)
    c.add_argument("--box", required=True, help="X,Y,W,H in pixels")
    c.set_defaults(func=cmd_crop)
```
with this in `verify.py`:
```python
def cmd_crop(args):
    import cuts
    src = resolve_source(args)
    if src.kind != "image":
        sys.exit("crop: works on images")
    print(cuts.crop(src.path, cuts.parse_box(args.box), dossier_dir(src.id) / "crops"))
```

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/pytest tests -q`
Expected: all pass (`test_crop_really_crops` runs ffmpeg).

- [ ] **Step 5: Real specimen with ground truth — a course slide**

`it-orderflow-0916-1108/slides.md` holds the slide at 0:19 ("Strong Buying / Selling Absorption"), frame-verified in dr-22w.2. Cut the same moment as a still, and ask the image path for its text:
```bash
cd media-reader
SRC="/mnt/c/Users/steve/OneDrive/Videos/Captures/Orderflow Trading Course _ InvestiTrade - Google Chrome 2026-09-16 11-08-12.mp4"
ffmpeg -y -v error -ss 25 -i "$SRC" -frames:v 1 /tmp/claude-slide-0025.png
.venv/bin/python mread.py ask --file /tmp/claude-slide-0025.png --id it-slide-smoke \
  --question "Transcribe the slide title and every bullet verbatim."
sed -n '/## 0:19/,/^## /p' dossiers/it-orderflow-0916-1108/slides.md
cd ..
```
Expected: the image path's title and bullets match `slides.md` word for word. View `/tmp/claude-slide-0025.png` with the Read tool as the third reader. If any two of the three readings disagree, report all three to Steve. Do not choose silently (doctrine rule 6).

- [ ] **Step 6: Commit**

```bash
git add media-reader tests
git commit -m "[dr-dqm.2] Images: inline bytes, ask --crop and crop for zooming"
```

---

### Task B4: Audio — local windows, `transcribe`, `fetch`

**Files:** `media-reader/perceive.py`, `mread.py`

- [ ] **Step 1: Write the failing test for re-basing**

Add to `tests/media_reader/test_cuts.py`:
```python
import perceive


def test_audio_claims_are_rebased_to_file_time():
    payload = {"claims": [{"t": "0:05"}, {"t": "1:10"}, {"t": None}]}
    perceive.rebase_claims(payload, 90)
    assert [c["t"] for c in payload["claims"]] == ["1:35", "2:40", None]
```
Run: `.venv/bin/pytest tests/media_reader/test_cuts.py -q`. Expected: `AttributeError: … 'rebase_claims'`.

- [ ] **Step 2: `ask` on an audio window**

In `perceive.py`:
```python
def rebase_claims(payload, offset):
    """A local cut starts at 0; the card speaks in file time."""
    for c in payload.get("claims") or []:
        if c.get("t"):
            c["t"] = fmt_ts(parse_ts(c["t"]) + offset)
```
In `cmd_ask`, after the crop block:
```python
    offset = 0
    if src.kind == "audio" and (args.start or args.end):
        a = parse_ts(args.start) if args.start else 0
        b = parse_ts(args.end) if args.end else probe_duration(src.path)
        if not b or b <= a:
            sys.exit("ask: give an --end after --start (duration unknown)")
        cut, offset = cuts.cut_audio(src.path, a, b, dossier_dir(src.id) / "chunks"), a
```
After `payload = gemini.parse_json_reply(…)`, add `if offset: rebase_claims(payload, offset)`, and record `"offset_s": offset` in `request.json`.

- [ ] **Step 3: `transcribe` for audio**

In `cmd_transcribe`, replace the Plan A guard with:
```python
    if src.kind == "audio":
        return transcribe_audio(args, src)
    if src.kind != "video":
        sys.exit(f"transcribe: {src.kind} sources are not supported "
                 "(YouTube videos get captions from fetch_transcripts.py)")
```
Change `t.add_argument("--file", required=True, …)` in `mread.py` to optional, and replace its `--file/--id` pair with `source_args(t)`. Then add:
```python
def transcribe_audio(args, src):
    """Chunked speech transcript of an audio file: each window is cut locally,
    uploaded once (cached per chunk), and re-based onto file time."""
    from google import genai
    from google.genai import types

    creds.require_key("mread.py")
    d = dossier_dir(src.id)
    total = probe_duration(src.path)
    start = parse_ts(args.start) if args.start else 0
    end = parse_ts(args.end) if args.end else total
    if not end:
        sys.exit("could not determine the file's duration; give --end")
    chunk = int(args.chunk * 60)
    windows = [(a, min(a + chunk, end)) for a in range(start, end, chunk)]
    client = genai.Client()
    segments, uncertainties, run_ids, models, tok_in, tok_out = [], [], [], set(), 0, 0
    for a, b in windows:
        print(f"[transcribe {fmt_ts(a)}-{fmt_ts(b)}]", file=sys.stderr)
        piece = cuts.cut_audio(src.path, a, b, d / "chunks")
        part = media_part(client, src, path=piece)
        answered, resp = gemini.generate_with_retry(
            client, args.model,
            types.Content(parts=[part, types.Part(text=AUDIO_TRANSCRIBE_PROMPT)]),
            gemini.media_config(None, response_mime_type="application/json"))
        models.add(answered)
        text, diag = gemini.response_text(resp, answered)
        payload = gemini.parse_json_reply(text, diag, {"segments": []})
        usage = getattr(resp, "usage_metadata", None)
        ts, run_dir = runs.new_run_dir(d)
        (run_dir / "request.json").write_text(json.dumps({
            "kind": "audio", "file": str(src.path), "mode": "transcribe",
            "model_requested": args.model, "model_answered": answered,
            "start": fmt_ts(a), "end": fmt_ts(b),
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "output_tokens": getattr(usage, "candidates_token_count", None),
        }, indent=2))
        (run_dir / "response.json").write_text(json.dumps(payload, indent=2))
        run_ids.append(ts)
        tok_in += getattr(usage, "prompt_token_count", 0) or 0
        tok_out += getattr(usage, "candidates_token_count", 0) or 0
        for seg in payload.get("segments") or []:
            seg["t"] = fmt_ts(parse_ts(seg.get("t") or "0") + a)
            segments.append(seg)
        for u in payload.get("uncertainties") or []:
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] {u}")
        if payload.get("raw_unparsed"):
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] reply not JSON; see runs/{ts}/")
        runs.append_run_log(src.card,
                            f"- {ts} [{fmt_ts(a)}-{fmt_ts(b)}] {answered} "
                            f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                            f"{getattr(usage, 'candidates_token_count', '?')}) — "
                            f"transcribe — runs/{ts}/")
    segments.sort(key=lambda x: parse_ts(x["t"]))
    (d / "transcript.json").write_text(json.dumps({
        "id": src.id, "kind": "audio", "file": str(src.path), "duration_s": total,
        "window": [fmt_ts(start), fmt_ts(end)], "chunk_s": chunk,
        "models": sorted(models), "prompt_tokens": tok_in, "output_tokens": tok_out,
        "runs": run_ids, "segments": segments, "uncertainties": uncertainties,
        "generated": datetime.now().isoformat(timespec="seconds"),
    }, indent=2, ensure_ascii=False))
    (d / "transcript.txt").write_text("\n".join(
        f"[{s['t']}] {s.get('speaker') or '?'}: {(s.get('speech') or '').strip()}"
        for s in segments) + "\n")
    print(f"{src.id}: {len(segments)} segments, {len(uncertainties)} uncertainties over "
          f"{len(windows)} chunk(s); tokens prompt={tok_in} output={tok_out}")
```
Add to `perceive.py`'s imports: `from prompts import AUDIO_TRANSCRIBE_PROMPT, ask_prompt` and `from sources import media_part, dossier_dir, probe_duration, resolve_source`.

- [ ] **Step 4: `fetch` — a podcast page to a local file**

In `perceive.py`:
```python
def cmd_fetch(args):
    """Download a podcast episode (any page yt-dlp understands) as audio into
    the dossier, remember it, and create the card. Interrogate with --id after."""
    import argparse as _ap
    if not sources.LOCAL_ID_RE.match(args.id or ""):
        sys.exit("fetch needs --id: a slug naming dossiers/<id>/")
    d = dossier_dir(args.id)
    ytdlp = Path(sys.executable).with_name("yt-dlp")
    ytdlp = str(ytdlp) if ytdlp.exists() else "yt-dlp"
    subprocess.run([ytdlp, "-x", "--audio-format", "m4a",
                    "-o", str(d / "source.%(ext)s"), args.url], check=True)
    got = sorted(d.glob("source.*"))
    got = [p for p in got if p.suffix != ".json"]
    if not got:
        sys.exit(f"yt-dlp produced no audio in {d}/")
    src = resolve_source(_ap.Namespace(file=str(got[0]), id=args.id, url=None,
                                       origin=args.url))
    print(f"{src.id}: {src.kind} {got[0].name} — card {src.card}")
```
Add `import sources` and `from pathlib import Path` if they are missing. In `mread.py`:
```python
    fe = sub.add_parser("fetch", help="download a podcast/audio page into a dossier")
    fe.add_argument("--url", required=True)
    fe.add_argument("--id", required=True)
    fe.set_defaults(func=cmd_fetch)
```

- [ ] **Step 5: Run the tests**

Run: `.venv/bin/pytest tests -q`
Expected: all pass.

- [ ] **Step 6: Real specimen with ground truth — the course's own audio**

`it-orderflow-0916-1339` has a `transcript.txt` made through the video path. Take its audio track and transcribe three minutes through the audio path:
```bash
cd media-reader
SRC="/mnt/c/Users/steve/OneDrive/Videos/Captures/Orderflow Trading Course _ InvestiTrade - Google Chrome 2026-09-16 13-39-46.mp4"
ffmpeg -y -v error -i "$SRC" -vn -c:a copy /tmp/claude-it-1339.m4a
.venv/bin/python mread.py transcribe --file /tmp/claude-it-1339.m4a --id it-audio-smoke --end 3:00 --chunk 1.5
head -12 dossiers/it-audio-smoke/transcript.txt
awk -F'[][]' '{split($2,t,":"); if (t[1]*60+t[2] < 180) print}' dossiers/it-orderflow-0916-1339/transcript.txt | head -12
cd ..
```
Expected: two transcripts of the same three minutes, one from the video path and one from the audio path. Numbers and trading terms should match verbatim. The chunk seam at 1:30 shows whether local cutting drops or duplicates words. Anything that differs goes into the B5 LESSONS entry with both versions. It also answers the doctrine question of whether the audio path is as reliable as the video path for speech.

- [ ] **Step 7: Commit**

```bash
git add media-reader tests
git commit -m "[dr-dqm.2] Audio: locally cut windows, ask with re-based timestamps, chunked transcribe, fetch"
```

---

### Task B5: Corpus and doctrine catch up

**Files:** `media-reader/corpus.py`, `media-reader/CLAUDE.md`, `media-reader/LESSONS.md`, `CLAUDE.md` (root)

- [ ] **Step 1: The oracle must stay quiet on the existing corpus**

Take the three smoke dossiers out of the way (they are kept for step 5):
```bash
mkdir -p /tmp/claude-dqm-smoke && mv media-reader/dossiers/{tb-letter-smoke,it-slide-smoke,it-audio-smoke} /tmp/claude-dqm-smoke/
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: four `identical`.

- [ ] **Step 2: INDEX tags non-video kinds; export knows the new verification words**

In `corpus.render_index`, change the two dossier link builders from:
```python
                link = f"[`{v['id']}`](dossiers/{v['id']}/CARD.md)"
```
to:
```python
                link = f"[`{v['id']}`](dossiers/{v['id']}/CARD.md)" + kind_tag(v)
```
(both the playlist-table and the shelved-table occurrences), and add:
```python
def kind_tag(v):
    """Videos are the corpus's default and stay untagged; other kinds say what they are."""
    k = v.get("kind", "youtube")
    return "" if k in ("youtube", "video") else f" · _{k}_"
```
Extend `VERIF_METHODS` (export):
```python
    ("quote_check", r"verify-quotes|quote[- ]check(?:ed)?"),
    ("page_image", r"\bpages-\d+-\d+\b|\bpage image\b"),
    ("crop", r"\bcrop-\d+-\d+-\d+x\d+\b|\bcrop(?:ped)?\b"),
    ("second_pass", r"second (?:pass|listen)|re-?listen"),
```

- [ ] **Step 2b: `build_corpus.py` must not invent a YouTube URL for other kinds**

Found in the B2 review: `build_corpus.py` gives every card `"url": "https://www.youtube.com/watch?v=<id>"`, so a document dossier gets a made-up YouTube link in `corpus.json` and in the reader. Read the card's `**Kind:**` field. Use the same fallback as `corpus.collect_videos`: `Kind`, else `youtube` when `URL` starts with `http`, else `video`. Emit `"kind"` on each card, and emit a YouTube `url` only for kind `youtube`; any other kind gets `null`. Check `build_reader.py` and `reader.template.html` for code that assumes a YouTube URL (cover images, "watch" links), and make them skip non-youtube kinds. The oracle must stay identical on the existing corpus, since every card there is youtube or video.

- [ ] **Step 3: Oracle again, then restore the smoke dossiers**

```bash
.venv/bin/python tests/media_reader/compare_outputs.py check
mv /tmp/claude-dqm-smoke/* media-reader/dossiers/
(cd media-reader && .venv/bin/python mread.py index --stdout | /usr/bin/grep -n 'smoke')
```
Expected: four `identical`. If `export.json` differs, a new verification regex matched existing card prose. Read the matched line: keep the change if the card really describes that method, otherwise tighten the regex. Then three index rows appear, tagged `· _document_`, `· _image_`, `· _audio_`.

- [ ] **Step 4: Write the doctrine down**

In `media-reader/CLAUDE.md`, after *Local captures*, add a section `## Other kinds: documents, images, audio`. It holds the verification table from the top of this plan, plus the commands:
```
mread.py ask --file F --id ID --question Q      # any kind; later calls: --id ID alone
mread.py verify-quotes --id ID [--run TS]      # documents: every quote must be in the text
mread.py pages --id ID --first N --last M      # PDFs: page images + text layer
mread.py crop --id ID --box X,Y,W,H            # images: a zoom box to look at yourself
mread.py ask --id ID --crop X,Y,W,H --question Q   # images: Gemini on the zoom box
mread.py ask --id ID --start MM:SS --end MM:SS --question Q   # audio: cut locally
mread.py transcribe --id ID [--chunk MIN]      # audio (and video captures)
mread.py fetch --url URL --id ID               # podcast page → dossier audio
```
It also says that new kinds use the `# Media:` card with `**Kind:**`, and that source files and cuts are gitignored because they are often private.

In the root `CLAUDE.md`, change the `media-reader/` row of Key Files to: *media ingestion: YouTube, local captures, audio, images, documents → verified dossiers (`mread.py`)*.

- [ ] **Step 5: Lessons from the three specimens**

Append to `media-reader/LESSONS.md`, one dated entry per kind, each `status: suspected`. State what the B2/B3/B4 specimens showed, with both versions quoted wherever readings disagreed. For audio, add the seam finding (words dropped or duplicated at the 1:30 cut, or neither). For documents, add how many quotes `verify-quotes` flagged `MISSING`, and why.

- [ ] **Step 6: Clean up specimens that are only tests**

```bash
rm -rf media-reader/dossiers/it-slide-smoke media-reader/dossiers/it-audio-smoke /tmp/claude-it-1339.m4a /tmp/claude-slide-0025.png
```
Keep `tb-letter-smoke` only if its card is worth curating. Otherwise remove it too. Then:
```bash
(cd media-reader && .venv/bin/python mread.py index && .venv/bin/python mread.py browse)
.venv/bin/pytest tests -q
```

- [ ] **Step 7: Commit, close, push**

```bash
git add -A media-reader CLAUDE.md tests
git commit -m "[dr-dqm.2] Corpus tags non-video kinds; export reads the new verification words; doctrine and lessons for documents, images, audio"
bd close dr-dqm.2
bd close dr-dqm
git pull --rebase && bd dolt push && git push && git status
```
Expected: `Your branch is up to date with 'origin/master'`.

---

## Done when

- `mread.py ask` answers about a PDF, a `.txt`/`.eml` letter, a PNG and an audio file, each with its own locator (page, region, timestamp).
- `verify-quotes`, `pages`, `crop` and audio windows exist, and each ran once against a real specimen whose answer was already known.
- The existing 58-card corpus's INDEX, export, browser and corpus outputs are unchanged, except for tags on the new kinds.
- LESSONS.md holds one `suspected` entry per new kind, from its specimen.

## Not in this plan (and why)

- **Gmail fetching as a source.** The newsletter ingester already pulls letters through the Gmail connector into `.txt`, and `mread.py` reads those. A `fetch --gmail` would duplicate that path. Revisit when a second mail source appears.
- **Scanned-PDF OCR.** Gemini reads scanned pages natively on the upload path. `verify-quotes` says when there is no text layer and points at `pages`.
- **Renaming the INDEX heading from "Video index"**, or regrouping by kind. Wait until the corpus holds enough non-video dossiers for the layout question to be real.
