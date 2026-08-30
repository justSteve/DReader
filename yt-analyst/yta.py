#!/usr/bin/env python3
"""yta.py v0.3 — YouTube analyst: Gemini Flash as a perception service.

Changes from v0.2:
  - Per-video dossiers: everything for a video lives under videos/<video_id>/.
    Each `ask` archives to videos/<id>/runs/<timestamp>/ and appends one line
    to the machine section of videos/<id>/CARD.md (created on first contact).
    `frames` outputs land under videos/<id>/ as well.
  - Curated card sections (Findings, Sessions, Lessons) belong to Claude Code /
    Steve; this script only ever appends to "## Run log" at the file's end.

Subcommands:
  ask     Interrogate a video (whole or clipped window). JSON out, archived.
  frames  Download a clip window and dump frames for pixel-level verification.
  index   Regenerate INDEX.md — every card, grouped by channel/author.

Requires: .env with GEMINI_API_KEY beside this script (or exported);
          `pip install google-genai`; yt-dlp + ffmpeg for frames.
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VIDEOS_DIR = SCRIPT_DIR / "videos"
DEFAULT_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-2.5-flash"]
RETRYABLE = {429, 500, 503}
MAX_ATTEMPTS = 4
BASE_DELAY_S = 5

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
_(machine-appended by yta.py — do not edit above this line's entries)_
"""


def load_env():
    """Load KEY=VALUE lines from .env beside this script. Existing env wins."""
    env_path = SCRIPT_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    # This tool's credential is GEMINI_API_KEY, full stop. An ambient
    # GOOGLE_API_KEY must never shadow it — evict it for this process.
    if os.environ.get("GEMINI_API_KEY"):
        os.environ.pop("GOOGLE_API_KEY", None)


def quiet_sdk():
    warnings.filterwarnings("ignore")
    for name in ("google_genai", "google.genai", "google_genai.models"):
        logging.getLogger(name).setLevel(logging.ERROR)


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
    d = VIDEOS_DIR / video_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensure_card(video_id, url):
    card = video_dir(video_id) / "CARD.md"
    if not card.exists():
        card.write_text(CARD_TEMPLATE.format(
            video_id=video_id, url=url,
            date=datetime.now().strftime("%Y-%m-%d")))
    return card


def append_run_log(card, line):
    with open(card, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def parse_ts(s):
    """'HH:MM:SS' | 'MM:SS' | '95' -> seconds."""
    if s is None:
        return None
    sec = 0
    for p in str(s).split(":"):
        sec = sec * 60 + int(p)
    return sec


def fmt_ts(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


def generate_with_retry(client, model, contents, config):
    """Call Gemini with backoff on transient errors, then model fallback.
    Returns (model_that_answered, response)."""
    from google.genai import errors
    import httpx

    chain = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_exc = None
    for m in chain:
        delay = BASE_DELAY_S
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                resp = client.models.generate_content(
                    model=m, contents=contents, config=config
                )
                return m, resp
            except (errors.APIError, httpx.TransportError) as e:
                # httpx.TransportError covers "Server disconnected without
                # sending a response" (RemoteProtocolError), read timeouts
                # and connect errors — seen 2026-08-29 under parallel asks
                # [dr-8qq.13]; treat like a 503.
                code = (getattr(e, "code", None) or getattr(e, "status_code", None)
                        or (503 if isinstance(e, httpx.TransportError) else None))
                if code in RETRYABLE:
                    last_exc = e
                    if attempt < MAX_ATTEMPTS:
                        print(f"[{m}: {code}; retry {attempt}/{MAX_ATTEMPTS - 1} "
                              f"in {delay}s]", file=sys.stderr)
                        time.sleep(delay)
                        delay *= 2
                else:
                    raise
        if m != chain[-1]:
            print(f"[{m}: exhausted retries; falling back]", file=sys.stderr)
    raise last_exc


def cmd_ask(args):
    from google import genai
    from google.genai import types

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY not set: add it to "
                 f"{SCRIPT_DIR / '.env'} or export it.")

    vid = extract_video_id(args.url)
    if not vid:
        sys.exit(f"Could not extract a YouTube video id from: {args.url}")
    url = canonical_url(vid)
    card = ensure_card(vid, url)

    client = genai.Client()

    vm_kwargs = {}
    if args.start is not None:
        vm_kwargs["start_offset"] = f"{parse_ts(args.start)}s"
    if args.end is not None:
        vm_kwargs["end_offset"] = f"{parse_ts(args.end)}s"
    if args.fps is not None:
        vm_kwargs["fps"] = args.fps

    video_part = types.Part(
        file_data=types.FileData(file_uri=url),
        video_metadata=types.VideoMetadata(**vm_kwargs) if vm_kwargs else None,
    )
    prompt = ANALYST_PROMPT.replace("{question}", args.question)

    cfg_kwargs = {"response_mime_type": "application/json"}
    if args.resolution:
        cfg_kwargs["media_resolution"] = {
            "low": types.MediaResolution.MEDIA_RESOLUTION_LOW,
            "medium": types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
            "high": types.MediaResolution.MEDIA_RESOLUTION_HIGH,
        }[args.resolution]

    answered_model, resp = generate_with_retry(
        client,
        args.model,
        types.Content(parts=[video_part, types.Part(text=prompt)]),
        types.GenerateContentConfig(**cfg_kwargs),
    )

    text = resp.text
    if text is None:
        # Empty response: blocked, truncated, or unprocessable video. Surface
        # the reason instead of dying in json.loads [dr-08s.9].
        cands = getattr(resp, "candidates", None) or []
        reasons = [str(getattr(c, "finish_reason", None)) for c in cands]
        fb = getattr(resp, "prompt_feedback", None)
        text = ""
        empty_diag = {"finish_reasons": reasons,
                      "prompt_feedback": str(fb) if fb else None}
        print(f"[empty response from {answered_model}: "
              f"finish_reasons={reasons} prompt_feedback={fb}]", file=sys.stderr)
    else:
        empty_diag = None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError:
            payload = {"summary": None, "claims": [], "uncertainties": [],
                       "raw_unparsed": text, "empty_response": empty_diag}

    usage = getattr(resp, "usage_metadata", None)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = video_dir(vid) / "runs" / ts
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:  # parallel asks can share a second; never overwrite an archive
        try:
            run_dir.mkdir()
            break
        except FileExistsError:
            n += 1
            ts = f"{ts.split('-')[0]}-{ts.split('-')[1]}-{n}"
            run_dir = run_dir.parent / ts
    (run_dir / "request.json").write_text(json.dumps({
        "url": url, "question": args.question,
        "model_requested": args.model, "model_answered": answered_model,
        "start": args.start, "end": args.end, "fps": args.fps,
        "resolution": args.resolution,
        "prompt_tokens": getattr(usage, "prompt_token_count", None),
        "output_tokens": getattr(usage, "candidates_token_count", None),
    }, indent=2))
    (run_dir / "response.json").write_text(json.dumps(payload, indent=2))

    window = (f" [{args.start or '0:00'}-{args.end or 'end'}]"
              if (args.start or args.end) else " [full]")
    q_short = (args.question[:80] + "…") if len(args.question) > 80 else args.question
    append_run_log(card,
                   f"- {ts}{window} {answered_model} "
                   f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                   f"{getattr(usage, 'candidates_token_count', '?')}) — "
                   f"Q: {q_short} — runs/{ts}/")

    print(json.dumps(payload, indent=2))
    print(f"\n[model: {answered_model}] [card: {card}] "
          f"[archived to {run_dir}/]", file=sys.stderr)
    if usage:
        print(f"[tokens: prompt={usage.prompt_token_count} "
              f"output={usage.candidates_token_count}]", file=sys.stderr)


def cmd_frames(args):
    vid = extract_video_id(args.url)
    if not vid:
        sys.exit(f"Could not extract a YouTube video id from: {args.url}")
    url = canonical_url(vid)
    start, end = parse_ts(args.start), parse_ts(args.end)

    out_dir = Path(args.out) if args.out else (
        video_dir(vid) / f"frames-{fmt_ts(start).replace(':', '')}-"
                         f"{fmt_ts(end).replace(':', '')}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Let yt-dlp choose the container (mp4/webm/mkv depending on the
    # selected streams) — a hardcoded .mp4 name gets a second extension
    # appended (clip.mp4.webm) and ffmpeg then can't find the file [dr-bot].
    for stale in out_dir.glob("clip.*"):
        stale.unlink()
    subprocess.run([
        "yt-dlp", "--download-sections", f"*{fmt_ts(start)}-{fmt_ts(end)}",
        # Prefer h264/mp4: ffmpeg's section download of YouTube's VP9/webm
        # DASH stream returned a clip with a zero-length video track
        # (frame=0) on 2026-08-29; avc1 mp4 sections decode and are ~7x
        # faster to fetch [dr-8qq.12].
        "-f", ("bv*[ext=mp4][vcodec^=avc1][height<=1080]+ba[ext=m4a]"
               "/bv*[ext=mp4][height<=1080]+ba"
               "/b[ext=mp4][height<=1080]/bv*[height<=1080]+ba/b[height<=1080]"),
        "--force-keyframes-at-cuts",
        "-o", str(out_dir / "clip.%(ext)s"), url,
    ], check=True)

    clips = sorted(out_dir.glob("clip.*"))
    if not clips:
        sys.exit(f"yt-dlp produced no clip in {out_dir}/")
    clip = clips[0]

    subprocess.run([
        "ffmpeg", "-y", "-i", str(clip),
        "-vf", f"fps={args.fps}",
        str(out_dir / "f_%04d.jpg"),
    ], check=True)

    n = len(list(out_dir.glob("f_*.jpg")))
    print(f"{n} frames in {out_dir}/ "
          f"(frame k ≈ t={fmt_ts(start)} + (k-1)/{args.fps}s)")


# ---------------------------------------------------------------- index ----
# Reads the curated header block of every videos/<id>/CARD.md and emits
# INDEX.md grouped by channel/author. Never reads below the first "## ".

INDEX_PATH = SCRIPT_DIR / "INDEX.md"
PLAYLISTS_DIR = SCRIPT_DIR / "playlists"

# Derived author names that should be folded together. Key and value are
# both compared case-insensitively; add an entry when the heuristic in
# author_of() splits one channel into two.
AUTHOR_ALIASES = {}

FIELD_RE = re.compile(r"\*\*([A-Za-z][A-Za-z ]*?):\*\*")
RUNLOG_RE = re.compile(r"^- (\d{8}-\d{6}) ")
PLAYLIST_ID_RE = re.compile(r"\b(PL[A-Za-z0-9_-]{5,})")
PLAYLIST_POS_RE = re.compile(r"#(\d+)")
SECONDS_RE = re.compile(r"\((\d+)\s*s\)")


def card_fields(text):
    """Parse '- **Key:** value' header lines above the first '## ' heading.

    Handles several fields on one line ('**Uploaded:** X · **Duration:** Y')
    by slicing between key markers, so a value that itself contains '·'
    (e.g. Playlist) survives intact.
    """
    fields = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        if not line.startswith("- **"):
            continue
        marks = list(FIELD_RE.finditer(line))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(line)
            val = line[m.end():end].strip().strip("·").strip()
            fields[m.group(1).strip()] = val
    return fields


def author_of(channel):
    """Canonical author key from a free-prose Channel field.

    'Carmine Rosato (Jumpstart Trading) — "Series" ep. 1' -> 'Carmine Rosato'
    'Smart Money Decode X (logo bottom-right; ...)'       -> 'Smart Money Decode X'
    """
    if not channel:
        return "(channel not recorded)"
    s = re.split(r"[—–]| - ", channel)[0]
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" ,;:·\"")
    s = s or "(channel not recorded)"
    return AUTHOR_ALIASES.get(s.lower(), s)


def duration_seconds(dur):
    """'26:24 (1584 s)' -> 1584. Falls back to parsing the MM:SS part."""
    if not dur:
        return 0
    m = SECONDS_RE.search(dur)
    if m:
        return int(m.group(1))
    m = re.match(r"(\d+):(\d{2})(?::(\d{2}))?", dur.strip())
    if not m:
        return 0
    a, b, c = m.group(1), m.group(2), m.group(3)
    return (int(a) * 3600 + int(b) * 60 + int(c)) if c else (int(a) * 60 + int(b))


def fmt_hm(sec):
    h, m = divmod(round(sec / 60), 60)
    return f"{h}h {m:02d}m" if h else f"{m}m"


def md_cell(s, limit=None):
    s = (s or "").replace("|", "\\|").replace("\n", " ").strip()
    if limit and len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s or "—"


def playlist_synthesis(pl_id):
    """Path (repo-relative) of the synthesis note for a playlist id, if any."""
    if not pl_id or not PLAYLISTS_DIR.is_dir():
        return None
    for p in sorted(PLAYLISTS_DIR.glob("*.md")):
        if pl_id in p.name or pl_id in p.read_text(errors="replace")[:2000]:
            return f"playlists/{p.name}"
    return None


def collect_videos():
    """One dict per videos/<id>/, whether or not it has a card."""
    out = []
    if not VIDEOS_DIR.is_dir():
        return out
    for d in sorted(VIDEOS_DIR.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir():
            continue
        card = d / "CARD.md"
        n_runs = len(list((d / "runs").glob("*/"))) if (d / "runs").is_dir() else 0
        if not card.exists():
            out.append({"id": d.name, "card": False, "runs": n_runs})
            continue
        text = card.read_text(errors="replace")
        f = card_fields(text)
        pl = f.get("Playlist", "")
        pl_id_m = PLAYLIST_ID_RE.search(pl)
        pos_m = PLAYLIST_POS_RE.search(pl)
        out.append({
            "id": d.name,
            "card": True,
            "title": f.get("Title", ""),
            "channel": f.get("Channel", ""),
            "author": author_of(f.get("Channel", "")),
            "uploaded": f.get("Uploaded", ""),
            "duration": (f.get("Duration", "") or "").split(" (")[0],
            "seconds": duration_seconds(f.get("Duration", "")),
            "status": f.get("Status", "").split()[0] if f.get("Status") else "",
            "analyzed": f.get("First analyzed", ""),
            "playlist_id": pl_id_m.group(1) if pl_id_m else "",
            "playlist_pos": int(pos_m.group(1)) if pos_m else 0,
            "runs": len(RUNLOG_RE.findall(text)) or n_runs,
        })
    return out


def render_index(vids):
    carded = [v for v in vids if v["card"]]
    orphans = [v for v in vids if not v["card"]]

    groups = {}
    for v in carded:
        groups.setdefault(v["author"], []).append(v)
    order = sorted(groups, key=lambda a: (-len(groups[a]), a.lower()))

    L = []
    L.append("# Video index")
    L.append("")
    L.append("_Generated by `yta.py index` from the header block of each "
             "`videos/<id>/CARD.md`. Do not edit by hand — rerun the command._")
    L.append("")
    L.append(f"**{len(carded)} videos** across **{len(order)} channels** · "
             f"{fmt_hm(sum(v['seconds'] for v in carded))} of runtime · "
             f"generated {datetime.now():%Y-%m-%d}.")
    L.append("")
    L.append("_`#` is the video's position in its playlist (not its episode "
             "number); `Runs` counts archived `ask` calls in the card's run log._")
    L.append("")
    L.append("| Channel | Videos | Uploads | Runtime | Open cards |")
    L.append("|---|---:|---|---:|---:|")
    for a in order:
        g = groups[a]
        dates = sorted(v["uploaded"] for v in g if v["uploaded"])
        span = (dates[0] if len(dates) == 1
                else f"{dates[0]} → {dates[-1]}") if dates else "—"
        n_open = sum(1 for v in g if v["status"] != "closed")
        L.append(f"| [{md_cell(a)}](#{slug(a)}) | {len(g)} | {span} | "
                 f"{fmt_hm(sum(v['seconds'] for v in g))} | {n_open} |")
    L.append("")

    for a in order:
        g = groups[a]
        dates = sorted(v["uploaded"] for v in g if v["uploaded"])
        n_open = sum(1 for v in g if v["status"] != "closed")
        L.append(f"## {a}")
        L.append("")
        bits = [f"{len(g)} video{'s' if len(g) != 1 else ''}"]
        if dates:
            bits.append(dates[0] if len(dates) == 1 else f"{dates[0]} → {dates[-1]}")
        bits.append(f"{fmt_hm(sum(v['seconds'] for v in g))} total")
        bits.append("all cards closed" if not n_open else f"{n_open} card(s) open")
        L.append(" · ".join(bits))
        L.append("")

        by_pl = {}
        for v in g:
            by_pl.setdefault(v["playlist_id"], []).append(v)
        # Playlists first (largest first), standalone videos last.
        pl_order = sorted((k for k in by_pl if k),
                          key=lambda k: (-len(by_pl[k]), k))
        if "" in by_pl:
            pl_order.append("")

        for pl in pl_order:
            rows = sorted(by_pl[pl],
                          key=lambda v: (v["playlist_pos"], v["uploaded"], v["id"]))
            if pl:
                syn = playlist_synthesis(pl)
                head = f"### Playlist `{pl}`"
                if syn:
                    head += f" — synthesis: [{syn}]({syn})"
                L.append(head)
            elif pl_order != [""]:
                L.append("### Standalone")
            if pl or pl_order != [""]:
                L.append("")
            L.append("| # | Video | Title | Uploaded | Len | Status | Runs |")
            L.append("|---:|---|---|---|---:|---|---:|")
            for v in rows:
                pos = str(v["playlist_pos"]) if v["playlist_pos"] else "—"
                link = f"[`{v['id']}`](videos/{v['id']}/CARD.md)"
                L.append(f"| {pos} | {link} | {md_cell(v['title'], 78)} | "
                         f"{md_cell(v['uploaded'])} | {md_cell(v['duration'])} | "
                         f"{md_cell(v['status'])} | {v['runs']} |")
            L.append("")

    if orphans:
        L.append("## No card yet")
        L.append("")
        L.append("_Video directories with archived runs but no `CARD.md` — "
                 "interrogated but never written up._")
        L.append("")
        L.append("| Video | Runs |")
        L.append("|---|---:|")
        for v in orphans:
            L.append(f"| [`{v['id']}`](videos/{v['id']}/) | {v['runs']} |")
        L.append("")

    return "\n".join(L).rstrip() + "\n"


def slug(s):
    """GitHub-style anchor for a heading."""
    return re.sub(r"[^a-z0-9\s-]", "", s.lower()).strip().replace(" ", "-")


def cmd_index(args):
    vids = collect_videos()
    md = render_index(vids)
    if args.stdout:
        sys.stdout.write(md)
        return
    INDEX_PATH.write_text(md)
    carded = sum(1 for v in vids if v["card"])
    authors = len({v["author"] for v in vids if v["card"]})
    print(f"{INDEX_PATH.name}: {carded} videos, {authors} channels"
          + (f", {len(vids) - carded} without a card" if carded != len(vids) else ""))


def main():
    load_env()
    quiet_sdk()

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("ask", help="interrogate video via Gemini")
    a.add_argument("--url", required=True)
    a.add_argument("--question", required=True)
    a.add_argument("--start", help="clip start (MM:SS or seconds)")
    a.add_argument("--end", help="clip end")
    a.add_argument("--fps", type=float, help="sampling fps (default 1; 0.1-60)")
    a.add_argument("--resolution", choices=["low", "medium", "high"])
    a.add_argument("--model", default=DEFAULT_MODEL)
    a.set_defaults(func=cmd_ask)

    f = sub.add_parser("frames", help="pull frames for verification")
    f.add_argument("--url", required=True)
    f.add_argument("--start", required=True)
    f.add_argument("--end", required=True)
    f.add_argument("--fps", type=float, default=1)
    f.add_argument("--out", help="output directory (default: videos/<id>/frames-*)")
    f.set_defaults(func=cmd_frames)

    i = sub.add_parser("index", help="regenerate INDEX.md from the cards")
    i.add_argument("--stdout", action="store_true",
                   help="print the index instead of writing INDEX.md")
    i.set_defaults(func=cmd_index)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
