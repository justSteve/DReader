"""Checking Gemini by pixels: `frames` cuts a window and dumps frames to compare against its claims."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import subprocess

from dreader_core.runs import parse_ts, fmt_ts  # noqa: E402
from sources import resolve_source, dossier_dir  # noqa: E402


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
