#!/usr/bin/env python3
"""mread.py v0.5 — media-reader: Gemini Flash as a perception service over media.

Changes from v0.4:
  - Renamed from yt-analyst/yta.py (dr-dqm); credentials, retry, uploads and
    run archives now come from dreader_core, shared with discord-reader.

Changes from v0.3:
  - Local captures (dr-22w.1): `ask`, `frames` and the new `transcribe`
    accept `--file PATH --id ID` in place of `--url`, for Game Bar
    recordings of members-only material (the InvestiTrade course). The file
    is uploaded once through the Gemini Files API and the handle cached in
    dossiers/<id>/upload.json for 48 h, so every zoom reuses it. On this path
    `--resolution` is a real lever (default = low; LESSONS.md 2026-09-12).
  - `transcribe` writes dossiers/<id>/transcript.{json,txt} and slides.md — the
    substrate READ.md is composed from — plus thumb.jpg, in chunks of
    --chunk minutes so no single reply outruns the output limit.

Changes from v0.2:
  - Per-video dossiers: everything for a video lives under dossiers/<video_id>/.
    Each `ask` archives to dossiers/<id>/runs/<timestamp>/ and appends one line
    to the machine section of dossiers/<id>/CARD.md (created on first contact).
    `frames` outputs land under dossiers/<id>/ as well.
  - Curated card sections (Findings, Sessions, Lessons) belong to Claude Code /
    Steve; this script only ever appends to "## Run log" at the file's end.

Subcommands:
  ask     Interrogate a video (whole or clipped window). JSON out, archived.
  frames  Download a clip window and dump frames for pixel-level verification.
  transcribe  Local capture -> timestamped speech + slide text (transcript.*).
  index   Regenerate INDEX.md — every card, grouped by channel/author.
  export  Emit the curated findings as JSON for sibling zgents.
  env     Say where the credential came from and whether it still works.

Requires: GEMINI_API_KEY in the vault file /home/vault/DReader/env, mode 0600;
          `pip install google-genai`; yt-dlp + ffmpeg for frames.
          When a call comes back unauthenticated, run `mread.py env` first.
"""

import argparse
import sys
from pathlib import Path

# The shared core lives at the repo root [dr-dqm].
_root = str(Path(__file__).resolve().parent.parent)  # after the tool's own dir, so a sibling module wins
if _root not in sys.path:
    sys.path.insert(1, _root)
from dreader_core import creds, gemini  # noqa: E402
from corpus import cmd_index, cmd_export, cmd_browse, BROWSER_PATH  # noqa: E402
from perceive import cmd_ask, cmd_transcribe, cmd_fetch  # noqa: E402
from sources import SCRIPT_DIR  # noqa: E402
from verify import cmd_frames, cmd_verify_quotes, cmd_pages, cmd_crop  # noqa: E402


def cmd_env(args):
    creds.report_env(SCRIPT_DIR, "mread.py", args.no_check)


def main():
    creds.load_env(SCRIPT_DIR)
    gemini.quiet_sdk()

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def source_args(sp):
        sp.add_argument("--url", help="YouTube URL")
        sp.add_argument("--file", help="local file: video, audio, image or document")
        sp.add_argument("--id", help="dossier id (slug); alone, reuses the file the dossier remembers")

    a = sub.add_parser("ask", help="interrogate video via Gemini")
    source_args(a)
    a.add_argument("--question", required=True)
    a.add_argument("--start", help="clip start (MM:SS or seconds)")
    a.add_argument("--end", help="clip end")
    a.add_argument("--fps", type=float, help="sampling fps (default 1; 0.1-60)")
    a.add_argument("--resolution", choices=["low", "medium", "high"])
    a.add_argument("--crop", help="images: X,Y,W,H pixel box to zoom on (sent instead of the whole image)")
    a.add_argument("--model", default=gemini.DEFAULT_MODEL)
    a.set_defaults(func=cmd_ask)

    f = sub.add_parser("frames", help="pull frames for verification")
    source_args(f)
    f.add_argument("--start", required=True)
    f.add_argument("--end", required=True)
    f.add_argument("--fps", type=float, default=1)
    f.add_argument("--out", help="output directory (default: dossiers/<id>/frames-*)")
    f.set_defaults(func=cmd_frames)

    cr = sub.add_parser("crop", help="images: cut a zoom box to dossiers/<id>/crops/ for viewing")
    source_args(cr)
    cr.add_argument("--box", required=True, help="X,Y,W,H in pixels")
    cr.set_defaults(func=cmd_crop)

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

    t = sub.add_parser("transcribe",
                       help="local capture or audio -> transcript.{json,txt} (+ slides.md for video)")
    source_args(t)
    t.add_argument("--start", help="window start (MM:SS); default 0")
    t.add_argument("--end", help="window end; default: file duration")
    t.add_argument("--chunk", type=float, default=10.0,
                   help="minutes per Gemini call (default 10)")
    t.add_argument("--fps", type=float, help="sampling fps (default 1)")
    t.add_argument("--resolution", choices=["low", "medium", "high"],
                   help="upload path honors this; default low")
    t.add_argument("--absolute", action="store_true",
                   help="model timestamps are file-absolute already (skip re-basing)")
    t.add_argument("--model", default=gemini.DEFAULT_MODEL)
    t.set_defaults(func=cmd_transcribe)

    fe = sub.add_parser("fetch", help="download a podcast/audio page into a dossier")
    fe.add_argument("--url", required=True)
    fe.add_argument("--id", required=True)
    fe.set_defaults(func=cmd_fetch)

    i = sub.add_parser("index", help="regenerate INDEX.md from the cards")
    i.add_argument("--stdout", action="store_true",
                   help="print the index instead of writing INDEX.md")
    i.set_defaults(func=cmd_index)

    b = sub.add_parser("browse", help="regenerate browser.html — the card reader")
    b.add_argument("--out", help=f"write here (default: {BROWSER_PATH.name})")
    b.set_defaults(func=cmd_browse)

    e = sub.add_parser("export", help="emit curated findings as JSON")
    e.add_argument("--out", help="write to this path (default: stdout)")
    e.add_argument("--video", action="append",
                   help="restrict to this video id (repeatable)")
    e.set_defaults(func=cmd_export)

    v = sub.add_parser("env", help="where the credential came from, and does it work")
    v.add_argument("--no-check", action="store_true",
                   help="skip the live call to Google")
    v.set_defaults(func=cmd_env)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
