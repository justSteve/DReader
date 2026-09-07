#!/usr/bin/env python3
"""Flatten videos/*/CARD.md into one corpus.json for the card-reader UI.

Reads ONLY the curated card text (never runs/), the same contract yta.py export
observes. Emits per-card metadata, the curated sections verbatim as markdown,
parsed grades, and the cross-reference edges between cards — the link graph the
cards have grown but that nothing currently surfaces.

Also reads videos/<id>/READ.md — the human-facing layer — into structured
fields: the L0 line, L1/L2 markdown, L3 passages (heading, timestamp, quotes)
with the editor asides pulled out as their own list; AUDIT.md into per-video
audit entries; and a per-card count of correction annotations.

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
AUDIT = ROOT / "AUDIT.md"
CORR_RE = re.compile(r"(?i:corrected 20\d\d-\d\d-\d\d)|\bAMENDED\b")
L3_HEAD_RE = re.compile(r"^\*\*(?P<h>.+?)\*\*\s*\*\((?P<ts>[^)]*)\)\*\s*$")
ASIDE_RE = re.compile(r"^\*\*Editor\s*[—–-]\*\*\s*")
VERIF_RE = re.compile(r"\b(un)?verified\b", re.I)


def count_verification(secs):
    """How the card marks its own findings: bare counts of the words the card
    uses, the same spellings yta.py export normalizes. Not a grade."""
    text = "\n".join(s["markdown"] for s in secs if s["name"].startswith("Findings"))
    marks = VERIF_RE.findall(text)
    return {
        "verified": sum(1 for m in marks if not m),
        "unverified": sum(1 for m in marks if m),
        "frames": len(re.findall(r"\bframes?\b|\bf_\d{3,4}\b", text)),
        "arithmetic": len(re.findall(r"arithmetic", text, re.I)),
    }


def _words(md):
    return len(re.findall(r"\S+", re.sub(r"[*_`>#\[\]()]", " ", md or "")))


def _ts_seconds(ts):
    m = re.match(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", ts or "")
    if not m:
        return None
    a, b, c = m.groups()
    return int(a) * 3600 + int(b) * 60 + int(c) if c else int(a) * 60 + int(b)


def _blocks(text):
    """Split a chunk of L3 markdown into blockquotes and plain paragraphs."""
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        if lines[i].lstrip().startswith(">"):
            q = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            body = "\n".join(q).strip()
            if ASIDE_RE.match(body):
                out.append({"kind": "aside", "markdown": ASIDE_RE.sub("", body, count=1)})
            else:
                out.append({"kind": "quote", "markdown": body})
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(">"):
                para.append(lines[i])
                i += 1
            out.append({"kind": "note", "markdown": "\n".join(para).strip()})
    return out


def parse_read(text):
    """READ.md -> the four levels as structured fields, asides pulled out."""
    head, *rest = re.split(r"^## ", text, flags=re.M)
    l0 = None
    m = re.search(r"^>\s*\*\*(.+?)\*\*\s*$", head, re.M | re.S)
    if m:
        l0 = " ".join(m.group(1).split())
    meta = {}
    for k, v in re.findall(r"\*\*([^:*]+):\*\*\s*([^·\n]*)", head):
        meta.setdefault(k.strip().lower(), v.strip().rstrip("·").strip())
    secs = {}
    for chunk in rest:
        name, _, body = chunk.partition("\n")
        secs[name.strip()] = body.strip()
    l1 = secs.get("In brief", "")
    l2 = secs.get("The argument", "")
    l3_name = next((n for n in secs if n.startswith("In ") and n.endswith(" words")), None)
    l3 = secs.get(l3_name, "") if l3_name else ""

    passages, asides = [], []
    cur = None
    for para in re.split(r"\n(?=\*\*[^*\n]+\*\*\s*\*\([^)]*\)\*\s*$)", "\n" + l3, flags=re.M):
        para = para.strip("\n")
        if not para.strip():
            continue
        first, _, body = para.partition("\n")
        hm = L3_HEAD_RE.match(first.strip())
        if hm:
            cur = {"heading": hm.group("h").strip(), "ts": hm.group("ts").strip(),
                   "ts_s": _ts_seconds(hm.group("ts")), "blocks": _blocks(body)}
        else:
            cur = {"heading": None, "ts": None, "ts_s": None, "blocks": _blocks(para)}
        for b in cur["blocks"]:
            if b["kind"] == "aside":
                asides.append({"passage": len(passages), "markdown": b["markdown"]})
        passages.append(cur)

    links = sorted(set(LINK_RE.findall(text)))
    return {
        "l0": l0,
        "meta": meta,
        "watch": (re.search(r"\*\*Watch:\*\*\s*(\S+)", head) or [None, None])[1],
        "l1_md": l1,
        "l2_md": l2,
        "l3_name": l3_name,
        "passages": passages,
        "asides": asides,
        "words": {"l0": _words(l0), "l1": _words(l1), "l2": _words(l2), "l3": _words(l3),
                  "total": _words(l0) + _words(l1) + _words(l2) + _words(l3)},
        "links_out": links,
    }


def parse_audit(text):
    """AUDIT.md -> {video_id: [entries]} plus the non-video sections."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    by_id, other = {}, []
    for i in range(1, len(parts), 2):
        heading, body = parts[i].strip(), parts[i + 1].strip()
        m = re.search(r"`([A-Za-z0-9_\-]{6,})`", heading)
        classes = re.findall(r"class ([\d, ]+)", heading)
        entry = {"heading": heading, "markdown": body,
                 "classes": [int(x) for x in re.findall(r"\d", classes[0])] if classes else [],
                 "clean": "clean" in heading}
        if m:
            by_id.setdefault(m.group(1), []).append(entry)
        else:
            other.append(entry)
    return by_id, other


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

        rf = vdir / "READ.md"
        read = parse_read(rf.read_text()) if rf.exists() else None
        if read:
            for target in read["links_out"]:
                if target != vdir.name and target not in {e["to"] for e in edges if e["from"] == vdir.name}:
                    edges.append({"from": vdir.name, "to": target, "via": "read"})

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
            "corrections": len(CORR_RE.findall(blob)),
            "verification": count_verification(secs),
            "read": read,
        })

    refs = []
    if PLAYLISTS.is_dir():
        for p in sorted(PLAYLISTS.glob("*.md")):
            t = p.read_text()
            title = next((l[2:].strip() for l in t.split("\n") if l.startswith("# ")), p.stem)
            refs.append({"file": p.name, "title": title, "markdown": t, "chars": len(t)})

    audit_by_id, audit_other = ({}, [])
    if AUDIT.exists():
        atext = AUDIT.read_text()
        audit_by_id, audit_other = parse_audit(atext)
        refs.append({"file": AUDIT.name, "title": "Transcript audit log", "markdown": atext,
                     "chars": len(atext)})
    for c in cards:
        c["audit"] = audit_by_id.get(c["id"], [])
    edits = ROOT / "EDITS.md"
    if edits.exists():
        etext = edits.read_text()
        refs.append({"file": edits.name, "title": "Scope edits log", "markdown": etext, "chars": len(etext)})

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
            "reads": sum(1 for c in cards if c["read"]),
            "asides": sum(len(c["read"]["asides"]) for c in cards if c["read"]),
            "corrections": sum(c["corrections"] for c in cards),
            "audited": len(audit_by_id),
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
    print(f"{out.name}: {c['cards']} cards ({c['graded']} graded, {c['reads']} read, "
          f"{c['audited']} audited), {c['edges']} links, {c['asides']} asides, "
          f"{c['corrections']} corrections, {c['channels']} channels, "
          f"{c['references']} reference docs, {out.stat().st_size/1024:.0f} KB")
