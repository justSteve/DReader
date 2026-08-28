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
            except errors.APIError as e:
                code = getattr(e, "code", None) or getattr(e, "status_code", None)
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
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError:
            payload = {"summary": None, "claims": [], "uncertainties": [],
                       "raw_unparsed": text}

    usage = getattr(resp, "usage_metadata", None)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = video_dir(vid) / "runs" / ts
    run_dir.mkdir(parents=True, exist_ok=True)
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
        "-f", "bv*[height<=1080]+ba/b[height<=1080]",
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

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
