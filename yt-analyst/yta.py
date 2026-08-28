#!/usr/bin/env python3
"""yta.py — YouTube analyst v0: Gemini Flash as a perception service.

Subcommands:
  ask     Interrogate a video (whole or clipped window). Returns JSON with
          timestamped claims. Raw responses archived under ./runs/.
  frames  Download a clip window and dump frames at the cited timestamps
          so a second pair of eyes (Claude) can verify claims against pixels.

Requires: GEMINI_API_KEY in env; `pip install google-genai`;
          yt-dlp + ffmpeg on PATH (frames subcommand only).

Examples:
  python yta.py ask --url https://youtu.be/VIDEO_ID \
      --question "What indicators are on the chart and what values do they show?"

  python yta.py ask --url https://youtu.be/VIDEO_ID \
      --start 12:40 --end 14:10 --fps 5 --resolution high \
      --question "Read every number visible on screen in this window."

  python yta.py frames --url https://youtu.be/VIDEO_ID --start 12:40 --end 14:10 --fps 1
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = os.environ.get("YTA_MODEL", "gemini-flash-latest")
RUNS_DIR = Path("runs")

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


def parse_ts(s: str) -> int:
    """'HH:MM:SS' | 'MM:SS' | '95' -> seconds."""
    if s is None:
        return None
    parts = [int(p) for p in str(s).split(":")]
    sec = 0
    for p in parts:
        sec = sec * 60 + p
    return sec


def fmt_ts(sec: int) -> str:
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


def cmd_ask(args):
    from google import genai
    from google.genai import types

    client = genai.Client()  # reads GEMINI_API_KEY

    vm_kwargs = {}
    if args.start is not None:
        vm_kwargs["start_offset"] = f"{parse_ts(args.start)}s"
    if args.end is not None:
        vm_kwargs["end_offset"] = f"{parse_ts(args.end)}s"
    if args.fps is not None:
        vm_kwargs["fps"] = args.fps

    video_part = types.Part(
        file_data=types.FileData(file_uri=args.url),
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

    resp = client.models.generate_content(
        model=args.model,
        contents=types.Content(
            parts=[video_part, types.Part(text=prompt)]
        ),
        config=types.GenerateContentConfig(**cfg_kwargs),
    )

    text = resp.text
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        # Strip accidental fences and retry once.
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError:
            payload = {"summary": None, "claims": [], "uncertainties": [],
                       "raw_unparsed": text}

    # Archive the run for the pipeline / bridge.
    run_dir = RUNS_DIR / datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "request.json").write_text(json.dumps({
        "url": args.url, "question": args.question, "model": args.model,
        "start": args.start, "end": args.end, "fps": args.fps,
        "resolution": args.resolution,
    }, indent=2))
    (run_dir / "response.json").write_text(json.dumps(payload, indent=2))

    print(json.dumps(payload, indent=2))
    print(f"\n[archived to {run_dir}/]", file=sys.stderr)
    usage = getattr(resp, "usage_metadata", None)
    if usage:
        print(f"[tokens: prompt={usage.prompt_token_count} "
              f"output={usage.candidates_token_count}]", file=sys.stderr)


def cmd_frames(args):
    start, end = parse_ts(args.start), parse_ts(args.end)
    if start is None or end is None:
        sys.exit("frames requires --start and --end")

    out_dir = Path(args.out or f"frames-{fmt_ts(start).replace(':', '')}-"
                               f"{fmt_ts(end).replace(':', '')}")
    out_dir.mkdir(parents=True, exist_ok=True)
    # Let yt-dlp choose the container (mp4/webm/mkv depending on the
    # selected streams) — a hardcoded .mp4 name gets a second extension
    # appended (clip.mp4.webm) and ffmpeg then can't find the file.
    for stale in out_dir.glob("clip.*"):
        stale.unlink()
    section = f"*{fmt_ts(start)}-{fmt_ts(end)}"
    subprocess.run([
        "yt-dlp", "--download-sections", section,
        "-f", "bv*[height<=1080]+ba/b[height<=1080]",
        "--force-keyframes-at-cuts",
        "-o", str(out_dir / "clip.%(ext)s"), args.url,
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
    f.add_argument("--out", help="output directory")
    f.set_defaults(func=cmd_frames)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
