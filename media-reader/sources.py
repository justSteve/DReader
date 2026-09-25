"""Where media comes from: YouTube ids and URLs, local captures, dossier dirs and cards."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
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
    bytes reach Gemini, and which verification commands apply. Plan B adds
    "audio", "image" and "document" kinds; nothing else in the tool names a
    kind directly [dr-dqm]."""
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


def resolve_source(args):
    """The Source named by --url or --file/--id; creates its card on first contact."""
    path = getattr(args, "file", None)
    if path:
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            sys.exit(f"--file: not a file: {path}")
        kind, mime = kind_for(path)
        vid = getattr(args, "id", None)
        if not vid or not LOCAL_ID_RE.match(vid):
            sys.exit("--file needs --id: a slug like it-orderflow-absorption-4142 "
                     "(lowercase letters, digits, hyphens; it names dossiers/<id>/)")
        if extract_video_id(vid + "x") and len(vid) == 11:
            sys.exit(f"--id {vid} looks like a YouTube id; pick a slug")
        card = dossier_dir(vid) / "CARD.md"
        if not card.exists():
            secs = probe_duration(path)
            card.write_text(CARD_TEMPLATE_LOCAL.format(
                video_id=vid, kind=kind, path=path, size_mb=path.stat().st_size / 1e6,
                duration=f"{fmt_ts(secs)} ({secs} s)" if secs else "duration unknown",
                date=datetime.now().strftime("%Y-%m-%d")))
        return Source(kind=kind, id=vid, card=card, path=path, mime=mime)
    url = getattr(args, "url", None)
    if not url:
        sys.exit("give --url (YouTube) or --file PATH --id ID (local capture)")
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
