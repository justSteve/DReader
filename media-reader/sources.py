"""Where media comes from: YouTube ids and URLs, local captures, dossier dirs and cards."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import re
import subprocess
from datetime import datetime

from dreader_core import uploads  # noqa: E402
from dreader_core.runs import fmt_ts  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
DOSSIERS_DIR = SCRIPT_DIR / "dossiers"


CARD_TEMPLATE = """# Video: {video_id}

- **URL:** {url}
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


def video_dir(video_id):
    d = DOSSIERS_DIR / video_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensure_card(video_id, url):
    card = video_dir(video_id) / "CARD.md"
    if not card.exists():
        card.write_text(CARD_TEMPLATE.format(
            video_id=video_id, url=url,
            date=datetime.now().strftime("%Y-%m-%d")))
    return card


CARD_TEMPLATE_LOCAL = """# Video: {video_id}

- **URL:** —
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
    """(video_id, url_or_None, local_path_or_None, card) from --url/--file."""
    path = getattr(args, "file", None)
    if path:
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            sys.exit(f"--file: not a file: {path}")
        vid = getattr(args, "id", None)
        if not vid or not LOCAL_ID_RE.match(vid):
            sys.exit("--file needs --id: a slug like it-orderflow-absorption-4142 "
                     "(lowercase letters, digits, hyphens; it names dossiers/<id>/)")
        if extract_video_id(vid + "x") and len(vid) == 11:
            sys.exit(f"--id {vid} looks like a YouTube id; pick a slug")
        card = video_dir(vid) / "CARD.md"
        if not card.exists():
            secs = probe_duration(path)
            card.write_text(CARD_TEMPLATE_LOCAL.format(
                video_id=vid, path=path, size_mb=path.stat().st_size / 1e6,
                duration=f"{fmt_ts(secs)} ({secs} s)" if secs else "duration unknown",
                date=datetime.now().strftime("%Y-%m-%d")))
        return vid, None, path, card
    url = getattr(args, "url", None)
    if not url:
        sys.exit("give --url (YouTube) or --file PATH --id ID (local capture)")
    vid = extract_video_id(url)
    if not vid:
        sys.exit(f"Could not extract a YouTube video id from: {url}")
    url = canonical_url(vid)
    return vid, url, None, ensure_card(vid, url)


def video_part_for(client, vid, url, path, vm_kwargs):
    from google.genai import types
    if path is not None:
        g = uploads.upload_cached(client, video_dir(vid) / "upload.json", path)
        fd = types.FileData(file_uri=g.uri, mime_type=g.mime_type)
    else:
        fd = types.FileData(file_uri=url)
    return types.Part(
        file_data=fd,
        video_metadata=types.VideoMetadata(**vm_kwargs) if vm_kwargs else None,
    )
