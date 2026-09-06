#!/usr/bin/env python3
"""Flatten videos/*/CARD.md into one corpus.json for the card-reader UI.

Reads ONLY the curated card text (never runs/), the same contract yta.py export
observes. Emits per-card metadata, the curated sections verbatim as markdown,
parsed grades, and the cross-reference edges between cards — the link graph the
cards have grown but that nothing currently surfaces.

  python3 build_corpus.py [--out corpus.json]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
PLAYLISTS = ROOT / "playlists"

MACHINE = "Run log"                      # never exposed as curated prose
GRADE_RE = re.compile(r"^\*\*(?P<axis>[A-Z][^:*]{2,60}):\s*(?P<val>[A-F][+−–\-]?)\.\*\*", re.M)
LINK_RE  = re.compile(r"\]\(\.\./([A-Za-z0-9_\-]{6,})/CARD\.md\)")
PLAY_RE  = re.compile(r"\]\((?:\.\./)*playlists/([A-Za-z0-9_.\-]+)\.md\)")


def _int(v):
    """'11,008' -> 11008; None/unparsable -> None."""
    if not v:
        return None
    digits = "".join(ch for ch in v if ch.isdigit())
    return int(digits) if digits else None


def _dur_seconds(v):
    """'28:28 (1708 s)' or '12:03' -> seconds."""
    if not v:
        return None
    import re as _re
    m = _re.search(r"(\d+):(\d{2})(?::(\d{2}))?", v)
    if not m:
        return None
    a, b, c = m.group(1), m.group(2), m.group(3)
    return int(a) * 3600 + int(b) * 60 + int(c) if c else int(a) * 60 + int(b)


def parse_header(text):
    """The `- **Key:** value` bullets above the first ## section."""
    head = text.split("\n## ", 1)[0]
    out = {}
    for line in head.split("\n"):
        for k, v in re.findall(r"\*\*([^:*]+):\*\*\s*([^·\n]*)", line):
            key = k.strip().lower().replace(" ", "_")
            val = v.strip().rstrip("·").strip()
            if val and key not in out:
                out[key] = val
    return out


def split_sections(text):
    """Ordered curated sections. The Run log is machine-appended: excluded."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    secs = []
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        body = parts[i + 1]
        # drop the italic placeholder line the skeleton ships with
        body = re.sub(r"^_\(.*?\)_\s*$", "", body, flags=re.M).strip()
        if name.startswith(MACHINE):
            continue
        if body:
            secs.append({"name": name, "markdown": body})
    return secs


def count_runs(vdir):
    r = vdir / "runs"
    return len([p for p in r.iterdir() if p.is_dir()]) if r.is_dir() else 0


def normalize_grade(v):
    """A− / A- / A–  ->  ('A', -1). Returns (letter, modifier, numeric)."""
    letter = v[0]
    mod = v[1:] if len(v) > 1 else ""
    step = 1 if mod == "+" else (-1 if mod in "−–-" else 0)
    base = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}[letter]
    numeric = base + step * 0.33
    return {"letter": letter, "modifier": "+" if step > 0 else ("−" if step < 0 else ""),
            "display": letter + ("+" if step > 0 else ("−" if step < 0 else "")),
            "numeric": round(numeric, 2)}


def build():
    cards, edges = [], []
    for vdir in sorted(p for p in VIDEOS.iterdir() if p.is_dir()):
        f = vdir / "CARD.md"
        if not f.exists():
            continue
        text = f.read_text()
        hdr = parse_header(text)
        secs = split_sections(text)
        blob = "\n".join(s["markdown"] for s in secs)

        grades = {}
        for m in GRADE_RE.finditer(blob):
            axis = m.group("axis").strip()
            key = ("clarity" if axis.lower().startswith("clarity")
                   else "alignment" if axis.lower().startswith("alignment")
                   else axis.lower().replace(" ", "_"))
            grades.setdefault(key, {"axis": axis, **normalize_grade(m.group("val"))})

        for target in set(LINK_RE.findall(blob)):
            if target != vdir.name:
                edges.append({"from": vdir.name, "to": target})

        cards.append({
            "id": vdir.name,
            "url": hdr.get("url", f"https://www.youtube.com/watch?v={vdir.name}"),
            "title": hdr.get("title"),
            "channel": hdr.get("channel"),
            "channel_key": (hdr.get("channel") or "").split("—")[0].split("(")[0].strip() or None,
            "uploaded": hdr.get("uploaded"),
            "duration": hdr.get("duration"),
            "duration_s": _dur_seconds(hdr.get("duration")),
            "views": _int(hdr.get("views")),
            "first_analyzed": hdr.get("first_analyzed"),
            "status": hdr.get("status"),
            "bead": hdr.get("bead"),
            "playlist": hdr.get("playlist") or hdr.get("sweep"),
            "playlist_refs": sorted(set(PLAY_RE.findall(blob))),
            "runs": count_runs(vdir),
            "grades": grades,
            "sections": secs,
            "section_names": [s["name"] for s in secs],
            "chars": len(blob),
        })

    refs = []
    if PLAYLISTS.is_dir():
        for p in sorted(PLAYLISTS.glob("*.md")):
            t = p.read_text()
            title = next((l[2:].strip() for l in t.split("\n") if l.startswith("# ")), p.stem)
            refs.append({"file": p.name, "title": title, "markdown": t, "chars": len(t)})

    ids = {c["id"] for c in cards}
    edges = [e for e in edges if e["to"] in ids]
    for c in cards:
        c["links_out"] = sorted({e["to"] for e in edges if e["from"] == c["id"]})
        c["links_in"] = sorted({e["from"] for e in edges if e["to"] == c["id"]})

    channels = {}
    for c in cards:
        channels.setdefault(c["channel_key"] or "(unknown)", []).append(c["id"])

    return {
        "generated": "build_corpus.py",
        "counts": {
            "cards": len(cards),
            "graded": sum(1 for c in cards if c["grades"]),
            "edges": len(edges),
            "channels": len(channels),
            "references": len(refs),
            "runs": sum(c["runs"] for c in cards),
        },
        "channels": [{"name": k, "cards": v} for k, v in sorted(channels.items(), key=lambda kv: -len(kv[1]))],
        "cards": cards,
        "edges": edges,
        "references": refs,
    }


if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "corpus.json"
    data = build()
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    c = data["counts"]
    print(f"{out.name}: {c['cards']} cards ({c['graded']} graded), {c['edges']} links, "
          f"{c['channels']} channels, {c['references']} reference docs, "
          f"{out.stat().st_size/1024:.0f} KB")
