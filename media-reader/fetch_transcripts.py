#!/usr/bin/env python3
"""Fetch YouTube auto-captions for every carded video into videos/<id>/transcript.txt.

Captions are the substrate for the human-facing READ.md layer: they carry the
presenter's own words, which the agent-facing CARD.md deliberately compresses
away. No Gemini API involved — yt-dlp only, so this is free to re-run.

Writes two files per video:
  transcript.txt   — de-duplicated plain text, one line per caption cue
  transcript.vtt   — the raw cue file, kept so timestamps stay recoverable

Auto-captions have two known failure modes, both handled downstream by the
composition spec rather than here (never silently "fix" a source):
  * native-English uploads come back unpunctuated and lowercase
  * AI-dubbed uploads are punctuated but mangle proper nouns
    (PbD -> "PVD", Vorwald -> "Forwald", Nill -> "Nelles")

  python3 fetch_transcripts.py [--force] [--only ID ...]
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
YTDLP = ROOT / ".venv" / "bin" / "yt-dlp"


def cues_to_text(vtt):
    """VTT -> plain text, dropping timing, tags and the rolling duplicates
    YouTube emits for its scrolling caption effect."""
    out, last = [], None
    for line in vtt.splitlines():
        line = line.strip()
        if not line or "-->" in line:
            continue
        if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line != last:
            out.append(line)
            last = line
    return "\n".join(out)


def fetch(vid, force=False):
    d = VIDEOS / vid
    txt, raw = d / "transcript.txt", d / "transcript.vtt"
    if txt.exists() and not force:
        return "skip", txt.stat().st_size
    tmp = d / "_cap"
    subprocess.run(
        [str(YTDLP), "--skip-download", "--write-auto-subs",
         "--sub-langs", "en-orig,en", "--sub-format", "vtt",
         "-o", str(tmp), f"https://www.youtube.com/watch?v={vid}"],
        capture_output=True, text=True, timeout=180,
    )
    got = sorted(d.glob("_cap*.vtt"))
    if not got:
        return "none", 0
    # prefer the original-language track when both exist
    pick = next((p for p in got if ".en-orig." in p.name), got[0])
    body = pick.read_text(encoding="utf-8", errors="replace")
    raw.write_text(body)
    txt.write_text(cues_to_text(body))
    for p in got:
        p.unlink()
    return "ok", txt.stat().st_size


if __name__ == "__main__":
    force = "--force" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
    ids = only or sorted(p.name for p in VIDEOS.iterdir()
                         if p.is_dir() and (p / "CARD.md").exists())
    tally = {}
    for vid in ids:
        try:
            status, size = fetch(vid, force)
        except Exception as e:
            status, size = "err", 0
            print(f"  !! {vid}: {e}", file=sys.stderr)
        tally[status] = tally.get(status, 0) + 1
        print(f"  {status:4s} {vid}  {size/1024:6.1f} KB")
    total = sum((VIDEOS / v / "transcript.txt").stat().st_size
                for v in ids if (VIDEOS / v / "transcript.txt").exists())
    print(f"\n{tally}  total {total/1024:.0f} KB across {len(ids)} videos")
