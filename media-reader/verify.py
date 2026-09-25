"""Checking Gemini by pixels: `frames` cuts a window and dumps frames to compare against its claims."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import json
import subprocess

from dreader_core.runs import parse_ts, fmt_ts  # noqa: E402
from sources import resolve_source, dossier_dir  # noqa: E402
import re  # noqa: E402

from documents import NO_TEXT_BODY, extract_text, page_count, quote_status  # noqa: E402


def cmd_frames(args):
    src = resolve_source(args)
    if src.kind not in ("youtube", "video"):
        sys.exit(f"frames: a {src.kind} source has no frames")
    start, end = parse_ts(args.start), parse_ts(args.end)

    out_dir = Path(args.out) if args.out else (
        dossier_dir(src.id) / f"frames-{fmt_ts(start).replace(':', '')}-"
                         f"{fmt_ts(end).replace(':', '')}")
    out_dir.mkdir(parents=True, exist_ok=True)

    if src.path is not None:
        # Local capture: cut straight from the file, no download step.
        # -ss before -i seeks by keyframe then decodes to the exact time.
        for stale in out_dir.glob("f_*.jpg"):
            stale.unlink()
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", str(start), "-to", str(end),
            "-i", str(src.path), "-vf", f"fps={args.fps}",
            str(out_dir / "f_%04d.jpg"),
        ], check=True)
        n = len(list(out_dir.glob("f_*.jpg")))
        print(f"{n} frames in {out_dir}/ "
              f"(frame k ≈ t={fmt_ts(start)} + (k-1)/{args.fps}s)")
        return

    # Let yt-dlp choose the container (mp4/webm/mkv depending on the
    # selected streams) — a hardcoded .mp4 name gets a second extension
    # appended (clip.mp4.webm) and ffmpeg then can't find the file [dr-bot].
    for stale in out_dir.glob("clip.*"):
        stale.unlink()
    # Resolve yt-dlp beside the running interpreter first: called from a
    # shell without the venv activated, a bare "yt-dlp" is not on PATH and
    # every window fails after the Gemini work was already paid for
    # (2026-09-08, LESSONS.md).
    ytdlp = Path(sys.executable).with_name("yt-dlp")
    ytdlp = str(ytdlp) if ytdlp.exists() else "yt-dlp"
    subprocess.run([
        ytdlp, "--download-sections", f"*{fmt_ts(start)}-{fmt_ts(end)}",
        # Prefer h264/mp4: ffmpeg's section download of YouTube's VP9/webm
        # DASH stream returned a clip with a zero-length video track
        # (frame=0) on 2026-08-29; avc1 mp4 sections decode and are ~7x
        # faster to fetch [dr-8qq.12].
        "-f", ("bv*[ext=mp4][vcodec^=avc1][height<=1080]+ba[ext=m4a]"
               "/bv*[ext=mp4][height<=1080]+ba"
               "/b[ext=mp4][height<=1080]/bv*[height<=1080]+ba/b[height<=1080]"),
        "--force-keyframes-at-cuts",
        "-o", str(out_dir / "clip.%(ext)s"), src.url,
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


_RUN_NAME = re.compile(r"^(\d{8})-(\d{6})(?:-(\d+))?$")


def latest_run(dossier, ts=None):
    runs_dir = dossier / "runs"
    if not runs_dir.is_dir():
        sys.exit(f"no runs/ under {dossier}/ — `ask` first")
    if ts:
        run = runs_dir / ts
        if not (run / "response.json").is_file():
            sys.exit(f"no run {ts} with a response.json under {runs_dir}/")
        return run

    # Run dirs are <date>-<time>[-n]; sort numerically on the collision
    # suffix so -10 follows -2 (plain name order would not) [Task 4 review].
    # Anything else sorts first, so it is never taken for the newest.
    def order(d):
        m = _RUN_NAME.match(d.name)
        if not m:
            return (0, d.name, "", 0)
        return (1, m[1], m[2], int(m[3] or 1))
    dirs = sorted((d for d in runs_dir.iterdir() if (d / "response.json").exists()),
                  key=order)
    if not dirs:
        sys.exit(f"no runs with a response.json under {runs_dir}/")
    return dirs[-1]


def cmd_verify_quotes(args):
    """Every verbatim quote in a run's claims must appear in the source text,
    and, for a PDF, on the page the claim names. Exit 1 if any is missing or
    on the wrong page — a finding, not a formatting nit."""
    src = resolve_source(args)
    if src.kind != "document":
        sys.exit(f"verify-quotes: {src.kind} sources have no text layer to check against")
    run = latest_run(dossier_dir(src.id), args.run)
    claims = json.loads((run / "response.json").read_text()).get("claims") or []
    text = extract_text(src.path)
    suf = src.path.suffix.lower()
    if suf == ".eml" and text.rstrip().endswith(NO_TEXT_BODY):
        sys.exit(f"verify-quotes: no text body in {src.path.name} — "
                 "the letter is images or attachments; read it by eye")
    if not text.strip():
        sys.exit(f"verify-quotes: no extractable text in {src.path.name} "
                 "(scanned PDF?) — use `pages` and read the page images")
    paged = suf == ".pdf"
    rows = [(c, quote_status(c, text, paged)) for c in claims if c.get("verbatim")]
    width = max([7] + [len(st) for _, st in rows])
    for c, st in rows:
        loc = f"p.{c['page']}" if c.get("page") else "   "
        print(f"{st:<{width}} {loc:>5}  {str(c['verbatim'])[:90]}")
    missing = sum(1 for _, st in rows if st == "MISSING")
    wrong = sum(1 for _, st in rows if st.startswith("WRONG PAGE"))
    print(f"\n{len(rows)} quoted claims in {run.name}: {len(rows) - missing - wrong} found, "
          f"{missing} missing, {wrong} on the wrong page; "
          f"{len(claims) - len(rows)} claims carry no quote")
    if not paged:
        print("page check: n/a (not a PDF)")
    sys.exit(1 if missing or wrong else 0)


def cmd_pages(args):
    """Render PDF pages to PNG (and their -layout text) for Claude to read."""
    src = resolve_source(args)
    if src.kind != "document" or src.path.suffix.lower() != ".pdf":
        sys.exit("pages: works on PDF documents")
    if args.first < 1:
        sys.exit(f"pages: --first {args.first}: pages start at 1")
    if args.first > args.last:
        sys.exit(f"pages: --first {args.first} is after --last {args.last}")
    n = page_count(src.path)
    if n is not None and args.last > n:
        sys.exit(f"pages: --last {args.last}, but {src.path.name} has {n} page(s)")
    out = dossier_dir(src.id) / f"pages-{args.first}-{args.last}"
    out.mkdir(parents=True, exist_ok=True)
    rng = ["-f", str(args.first), "-l", str(args.last)]
    subprocess.run(["pdftoppm", *rng, "-r", str(args.dpi), "-png", str(src.path),
                    str(out / "p")], check=True)
    subprocess.run(["pdftotext", *rng, "-layout", str(src.path), str(out / "text.txt")],
                   check=True)
    print(f"{len(list(out.glob('p-*.png')))} page image(s) + text.txt in {out}/")
