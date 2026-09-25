"""Where media comes from: YouTube ids and URLs, local captures, dossier dirs and cards."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime

from dreader_core import uploads  # noqa: E402
from dreader_core.runs import fmt_ts  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
DOSSIERS_DIR = SCRIPT_DIR / "dossiers"


@dataclass
class Source:
    """One piece of media and its dossier. `kind` decides the prompt, how the
    bytes reach Gemini, and which verification commands apply. New kinds are
    added in KIND_BY_EXT and branch on `src.kind` where behaviour differs
    (media_part, the ask/transcribe/frames guards) [dr-dqm]."""
    kind: str               # "youtube" | "video"
    id: str
    card: Path
    url: str | None = None
    path: Path | None = None
    mime: str | None = None


# Local file kinds, by extension. Plan B extends this table; the error message
# for an unknown extension lists whatever it holds.
KIND_BY_EXT = {
    ".mp4": ("video", "video/mp4"),
    ".mkv": ("video", "video/x-matroska"),
    ".mov": ("video", "video/quicktime"),
    ".webm": ("video", "video/webm"),
}
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


def kind_for(path):
    try:
        return KIND_BY_EXT[path.suffix.lower()]
    except KeyError:
        sys.exit(f"--file: unsupported type {path.suffix or '(none)'}; "
                 f"known: {' '.join(sorted(KIND_BY_EXT))}")


CARD_TEMPLATE = """# Video: {video_id}

- **URL:** {url}
- **Kind:** youtube
- **First analyzed:** {date}
- **Status:** open

## Findings
_(curated by Claude Code: verified findings with timestamps)_

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
"""


def extract_video_id(url):
    for pat in (r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
                r"(?:embed/)([a-zA-Z0-9_-]{11})",
                r"(?:shorts/)([a-zA-Z0-9_-]{11})"):
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def canonical_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


def dossier_dir(video_id):
    d = DOSSIERS_DIR / video_id
    d.mkdir(parents=True, exist_ok=True)
    return d


video_dir = dossier_dir  # the pre-dr-dqm name, kept for any external caller


def ensure_card(video_id, url):
    card = dossier_dir(video_id) / "CARD.md"
    if not card.exists():
        card.write_text(CARD_TEMPLATE.format(
            video_id=video_id, url=url,
            date=datetime.now().strftime("%Y-%m-%d")))
    return card


CARD_TEMPLATE_LOCAL = """# Video: {video_id}

- **URL:** —
- **Kind:** {kind}
- **Source:** local capture `{path}` ({size_mb:.0f} MB, {duration})
- **First analyzed:** {date}
- **Status:** open

## Findings
_(curated by Claude Code: verified findings with timestamps)_

## Sessions
_(curated by Claude Code: one entry per interrogation session — date, aim, verdict)_

## Lessons (this video)
_(anything peculiar to this video/channel: layout, chart software, segment structure)_

## Run log
_(machine-appended by mread.py — do not edit above this line's entries)_
"""

LOCAL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,60}$")


def probe_duration(path):
    """Seconds, via ffprobe; 0 if it cannot tell."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        return int(float(out))
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return 0


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


def media_part(client, src, vm_kwargs):
    """The Part that carries src's bytes to Gemini."""
    from google.genai import types
    if src.kind == "youtube":
        fd = types.FileData(file_uri=src.url)
    else:
        g = uploads.upload_cached(client, dossier_dir(src.id) / "upload.json",
                                  src.path, src.mime)
        fd = types.FileData(file_uri=g.uri, mime_type=g.mime_type)
    return types.Part(
        file_data=fd,
        video_metadata=types.VideoMetadata(**vm_kwargs) if vm_kwargs else None,
    )
