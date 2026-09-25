"""The corpus views over the cards: INDEX.md, the findings export, browser.html."""

import sys
from pathlib import Path
import json
import re
from datetime import datetime

import sources
from sources import SCRIPT_DIR


# ---------------------------------------------------------------- index ----
# Reads the curated header block of every dossiers/<id>/CARD.md and emits
# INDEX.md grouped by channel/author. Never reads below the first "## ".

INDEX_PATH = SCRIPT_DIR / "INDEX.md"
PLAYLISTS_DIR = SCRIPT_DIR / "playlists"

# Derived author names that should be folded together. Key and value are
# both compared case-insensitively; add an entry when the heuristic in
# author_of() splits one channel into two.
AUTHOR_ALIASES = {}

FIELD_RE = re.compile(r"\*\*([A-Za-z][A-Za-z ]*?):\*\*")
RUNLOG_RE = re.compile(r"^- (\d{8}-\d{6}) ")
PLAYLIST_ID_RE = re.compile(r"\b(PL[A-Za-z0-9_-]{5,}|course-[a-z0-9]+(?:-[a-z0-9]+)*)")
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
    """One dict per dossiers/<id>/, whether or not it has a card."""
    out = []
    if not sources.DOSSIERS_DIR.is_dir():
        return out
    for d in sorted(sources.DOSSIERS_DIR.iterdir(), key=lambda p: p.name.lower()):
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
            "kind": f.get("Kind") or ("youtube" if (f.get("URL") or "").startswith("http") else "video"),
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


def kind_tag(v):
    """Videos are the corpus's default and stay untagged; other kinds say what they are."""
    k = v.get("kind", "youtube")
    return "" if k in ("youtube", "video") else f" · _{k}_"


def render_index(vids):
    shelved = [v for v in vids if v["card"] and v["status"] == "shelved"]
    carded = [v for v in vids if v["card"] and v["status"] != "shelved"]
    orphans = [v for v in vids if not v["card"]]

    groups = {}
    for v in carded:
        groups.setdefault(v["author"], []).append(v)
    order = sorted(groups, key=lambda a: (-len(groups[a]), a.lower()))

    L = []
    L.append("# Video index")
    L.append("")
    L.append("_Generated by `mread.py index` from the header block of each "
             "`dossiers/<id>/CARD.md`. Do not edit by hand — rerun the command._")
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
                link = f"[`{v['id']}`](dossiers/{v['id']}/CARD.md)" + kind_tag(v)
                L.append(f"| {pos} | {link} | {md_cell(v['title'], 78)} | "
                         f"{md_cell(v['uploaded'])} | {md_cell(v['duration'])} | "
                         f"{md_cell(v['status'])} | {v['runs']} |")
            L.append("")

    if shelved:
        L.append("## Shelved")
        L.append("")
        L.append("_Cards kept for reference but withdrawn from the browser and "
                 "reader — assessed and found not worth the corpus's attention. "
                 "Read the card before starting on the same channel again._")
        L.append("")
        L.append("| Channel | Video | Title | Uploaded | Len | Runs |")
        L.append("|---|---|---|---|---:|---:|")
        for v in sorted(shelved, key=lambda v: (v["author"].lower(), v["uploaded"])):
            link = f"[`{v['id']}`](dossiers/{v['id']}/CARD.md)" + kind_tag(v)
            L.append(f"| {md_cell(v['author'])} | {link} | {md_cell(v['title'], 78)} | "
                     f"{md_cell(v['uploaded'])} | {md_cell(v['duration'])} | {v['runs']} |")
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
            L.append(f"| [`{v['id']}`](dossiers/{v['id']}/) | {v['runs']} |")
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
    shown = [v for v in vids if v["card"] and v["status"] != "shelved"]
    shelved = sum(1 for v in vids if v["card"] and v["status"] == "shelved")
    orphans = sum(1 for v in vids if not v["card"])
    authors = len({v["author"] for v in shown})
    print(f"{INDEX_PATH.name}: {len(shown)} videos, {authors} channels"
          + (f", {shelved} shelved" if shelved else "")
          + (f", {orphans} without a card" if orphans else ""))


# --------------------------------------------------------------- export ----
# Machine-readable view of the CURATED card sections, for sibling zgents.
# Never reads runs/ (raw, unverified, pre-curation) and never invents a value
# the cards do not carry: fields the format cannot supply are emitted as null
# with the reason stated in the envelope's `contract` block [dr-shu].

EXPORT_SCHEMA_VERSION = 2

VERIF_METHODS = [
    ("frames", r"\bframes?\b|\bin-frame\b|\bf_\d{3,4}\b"),
    ("arithmetic", r"arithmetic"),
    ("parity", r"parity"),
    ("cross_episode", r"cross[- ]episode|cross[- ]video"),
    ("quote_check", r"verify-quotes|quote[- ]check(?:ed)?"),
    ("page_image", r"\bpages-\d+-\d+\b|\bpage image\b"),
    ("crop", r"\bcrop-\d+-\d+-\d+x\d+\b"),
    ("second_pass", r"second (?:pass|listen)|re-?listen"),
]
# Cards mark verification in prose as well as in bold: "**Verified: frames**",
# "(verified)", "verified in-frame", "(Slides unverified.)". Match the bare
# word and read methods from the words around it.
VERIF_WORD_RE = re.compile(r"\b(?P<un>un)?verified\b", re.I)
FRAME_QUAL_RE = re.compile(r"(frames-[\w-]+)/(f_\d{3,4})(?:\.jpg)?")
FRAME_BARE_RE = re.compile(r"\bf_(\d{3,4})(?:\.jpg)?\b")
FRAME_DIR_RE = re.compile(r"\bframes-[\w-]+\b")
TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")


GROUP_HEADER_RE = re.compile(r"^\*\*[^*]+:\*\*$")


def findings_blocks(text):
    """Split the curated '## Findings' body into candidate finding records.

    A block starts at a top-level bullet ('- ') or a bold lead-in ('**').
    Continuation and nested lines stay with their parent.

    A block that is ONLY a bold phrase ending in a colon is a GROUP HEADER,
    not a finding — e.g. '**Slides (all verified word-for-word by frames
    unless noted):**'. It is not emitted, and its verification statement is
    inherited by the blocks beneath it (until the next header) so the grade
    travels to the findings it actually covers. A block with prose after the
    bold run is a finding, not a header.

    Yields (index, block_text, header_text_or_None).
    """
    m = re.search(r"^## Findings\s*$(.*?)^## ", text, re.S | re.M)
    if not m:
        return []
    body = m.group(1)
    blocks, cur = [], []
    for line in body.splitlines():
        if re.match(r"^_\(curated", line.strip()):   # section caption
            continue
        starts = line.startswith("- ") or line.startswith("**")
        if starts and cur:
            blocks.append("\n".join(cur))
            cur = [line]
        elif starts:
            cur = [line]
        elif cur:
            cur.append(line)
        elif line.strip():
            cur = [line]
    if cur:
        blocks.append("\n".join(cur))

    out, header = [], None
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if GROUP_HEADER_RE.match(b.replace("\n", " ").strip()):
            header = b.replace("\n", " ").strip()
            continue
        out.append((len(out), b, header))
    return out


def parse_verification(block):
    """Normalize the card's many verification spellings into one shape.

    grade: verified | unverified | mixed | unknown. 'unknown' means the card
    marks nothing — it is NOT a synonym for unverified and a consumer must
    never collapse the two.
    """
    marks = list(VERIF_WORD_RE.finditer(block))
    pos = [m for m in marks if not m.group("un")]
    neg = [m for m in marks if m.group("un")]
    grade = ("mixed" if pos and neg else
             "verified" if pos else
             "unverified" if neg else "unknown")

    # Methods come from the words around each positive marker, not the whole
    # block: "unverified ... elsewhere frames" must not read as verified+frames.
    ctx = " ".join(block[max(0, m.start() - 40):m.end() + 90] for m in pos)
    methods = [name for name, pat in VERIF_METHODS if re.search(pat, ctx, re.I)]

    dirs = sorted(set(FRAME_DIR_RE.findall(block)))
    frames = {f"{d}/{f}.jpg" for d, f in FRAME_QUAL_RE.findall(block)}
    # Cards cite follow-on frames bare ("frames-615-640/f_0004.jpg, f_0013.jpg"
    # or "**verified** f_0012"). Qualify them only when the block names exactly
    # one directory; otherwise the attachment is genuinely ambiguous.
    bare = {f"f_{n}" for n in FRAME_BARE_RE.findall(block)}
    bare -= {f for _, f in FRAME_QUAL_RE.findall(block)}
    unqualified = []
    if bare:
        if len(dirs) == 1:
            frames |= {f"{dirs[0]}/{b}.jpg" for b in bare}
        else:
            unqualified = sorted(bare)
    return {
        "grade": grade,
        "methods": methods,
        "frames": sorted(frames),
        "frame_dirs": dirs,
        "frames_unqualified": unqualified,
    }


def build_export(vids):
    import hashlib
    findings, videos = [], []
    for v in vids:
        if not v["card"]:
            continue
        card_rel = f"dossiers/{v['id']}/CARD.md"
        videos.append({k: v[k] for k in (
            "id", "title", "channel", "author", "uploaded", "duration",
            "seconds", "status", "playlist_id", "playlist_pos", "runs")}
            | {"card_path": card_rel})
        text = (sources.DOSSIERS_DIR / v["id"] / "CARD.md").read_text(errors="replace")
        for idx, block, header in findings_blocks(text):
            body = re.sub(r"\s+", " ", block.lstrip("- ").strip())
            verif = parse_verification(block)
            if verif["grade"] == "unknown" and header:
                inherited = parse_verification(header)
                if inherited["grade"] != "unknown":
                    verif = dict(inherited, frames=verif["frames"],
                                 frame_dirs=verif["frame_dirs"],
                                 frames_unqualified=verif["frames_unqualified"],
                                 inherited_from=header)
            findings.append({
                # No stable id: the card format carries none, and a synthesized
                # one would look stable without being so. See contract below.
                "id": None,
                "locator": {"card_path": card_rel,
                            "section": "Findings",
                            "block_index": idx},
                "text_sha256": hashlib.sha256(body.encode()).hexdigest()[:16],
                "video_id": v["id"],
                "channel": v["channel"],
                "author": v["author"],
                "playlist_id": v["playlist_id"] or None,
                "playlist_position": v["playlist_pos"] or None,
                "card_path": card_rel,
                "card_status": v["status"] or None,
                "text": body,
                "timestamps": sorted(set(TIMESTAMP_RE.findall(block))),
                "kind": None,
                "verification": verif,
                "attachment": None,
            })
    return {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "generator": "mread.py export",
        "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "contract": {
            "changes_from_v1": "card paths moved from videos/<id>/ to "
                               "dossiers/<id>/ (dr-dqm, 2026-09-25); ids unchanged",
            "source": "curated '## Findings' sections of dossiers/<id>/CARD.md only",
            "never_exported": "dossiers/*/runs/ — raw model output, unverified, "
                              "pre-curation. Do not consume it.",
            "id": "null. The card format carries no per-finding id. A "
                  "synthesized id would look stable across card revisions "
                  "without being so, so none is emitted. Use `locator` to "
                  "find a record and `text_sha256` to detect that it changed; "
                  "neither is a durable key. Re-keying will be needed if ids "
                  "are ever added to the card format.",
            "kind": "null. The onscreen_text/visual/spoken/inferred taxonomy "
                    "exists in runs/*.json, not in the curated cards.",
            "attachment": "null. What a figure was attached to (which chart, "
                          "panel or ladder) is present in `text` as prose but "
                          "is not a card field. Its absence is a real gap: "
                          "every other check validates the number, so a "
                          "correctly-read value on the wrong chart passes "
                          "them all.",
            "verification.grade": "verified | unverified | mixed | unknown. "
                                  "'unknown' means the card marks nothing and "
                                  "is NOT a synonym for 'unverified' — about "
                                  "half of all blocks are unknown. Never "
                                  "collapse the two.",
            "block_granularity": "One record per top-level bullet or bold "
                                 "lead-in paragraph. Blocks are prose and may "
                                 "carry several claims; a block is not a claim.",
            "verification.inherited_from": "Present when the grade came from a "
                                           "group header covering this block "
                                           "(e.g. '**Slides (all verified by "
                                           "frames unless noted):**') rather "
                                           "than from the block's own text. A "
                                           "block that states its own grade "
                                           "always wins over the header.",
            "verification.frames_unqualified": "Frame ids the card cited bare "
                                               "(f_0013) where the block named "
                                               "more than one frames-* dir, so "
                                               "the directory is ambiguous. Not "
                                               "guessed.",
        },
        "videos": videos,
        "findings": findings,
    }


def cmd_export(args):
    data = build_export(collect_videos())
    if args.video:
        keep = set(args.video)
        data["videos"] = [v for v in data["videos"] if v["id"] in keep]
        data["findings"] = [f for f in data["findings"] if f["video_id"] in keep]
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(text)
        g = sum(1 for f in data["findings"]
                if f["verification"]["grade"] == "unknown")
        print(f"{args.out}: {len(data['findings'])} findings from "
              f"{len(data['videos'])} cards ({g} with grade 'unknown')")
    else:
        sys.stdout.write(text)


# --------------------------------------------------------------- browse ----
# A single self-contained HTML file for reading the corpus: a sortable,
# filterable table of every video, and a reading view for any card, the
# generated index or a playlist synthesis. No network, no assets, no server —
# open it in a browser, where Ctrl+wheel and Ctrl+± are the browser's own
# zoom. Regenerate whenever cards change; it is a snapshot, so it is
# gitignored [dr-s0p].

BROWSER_PATH = SCRIPT_DIR / "browser.html"


def _card_body(text):
    """Everything from the first '## ' section on — the curated prose."""
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("## "):
            return "\n".join(lines[i:]).strip()
    return text.strip()


YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def browse_documents():
    """Every document the browser shows, plus the source list and totals."""
    vids = collect_videos()
    docs = []

    for v in vids:
        d = sources.DOSSIERS_DIR / v["id"]
        if v["card"] and v["status"] == "shelved":
            continue   # kept on disk and in INDEX.md's Shelved section, not shown
        if not v["card"]:
            docs.append({
                "key": f"v:{v['id']}", "kind": "video", "id": v["id"],
                "title": "(no card written)", "source": "(no card)",
                "channel": "", "uploaded": "", "duration": "", "seconds": 0,
                "status": "no card", "pos": 0, "playlist": "", "runs": v["runs"],
                "url": (f"https://www.youtube.com/watch?v={v['id']}"
                        if YOUTUBE_ID_RE.match(v["id"]) else ""),
                "file": f"dossiers/{v['id']}/",
                "body": (f"_No `CARD.md` yet — {v['runs']} archived run"
                         f"{'' if v['runs'] == 1 else 's'} under "
                         f"`dossiers/{v['id']}/runs/`, never written up._"),
            })
            continue
        text = (d / "CARD.md").read_text(errors="replace")
        url = card_fields(text).get("URL", "") or ""
        # Only a YouTube card has somewhere to watch; a local capture's "—" or a
        # document's missing URL must not become a "watch on YouTube" link.
        url = url if v["kind"] == "youtube" and url.startswith("http") else ""
        docs.append({
            "key": f"v:{v['id']}", "kind": "video", "id": v["id"],
            "title": v["title"], "source": v["author"], "channel": v["channel"],
            "uploaded": v["uploaded"].split(" ")[0], "duration": v["duration"],
            "seconds": v["seconds"], "status": v["status"] or "closed",
            "pos": v["playlist_pos"], "playlist": v["playlist_id"],
            "runs": v["runs"],
            "url": url,
            "file": f"dossiers/{v['id']}/CARD.md",
            "body": _card_body(text),
        })

    refs = [{
        "key": "index", "kind": "index", "id": "INDEX.md", "title": "Video index",
        "source": "", "file": "INDEX.md", "url": "",
        "subtitle": "generated from every card header — do not hand-edit",
        "body": INDEX_PATH.read_text(errors="replace") if INDEX_PATH.exists() else "",
    }]
    if PLAYLISTS_DIR.is_dir():
        for p in sorted(PLAYLISTS_DIR.glob("*.md")):
            body = p.read_text(errors="replace")
            m = re.search(r"^# (.*)$", body, re.M)
            title = (m.group(1) if m else p.stem)
            docs_in = ", ".join(sorted({
                v["author"] for v in vids
                if v["card"] and v["playlist_id"] and v["playlist_id"] in p.name
            }))
            refs.append({
                "key": f"p:{p.name}", "kind": "playlist", "id": p.name,
                "title": re.sub(r"^Playlist synthesis — ", "", title),
                "source": docs_in, "file": f"playlists/{p.name}", "url": "",
                "subtitle": "what the whole series adds up to, across its cards",
                "body": body,
            })

    carded = [d for d in docs if d["status"] != "no card"]
    counts = {}
    for d in docs:
        counts[d["source"]] = counts.get(d["source"], 0) + 1
    source_names = sorted(counts, key=lambda s: (s == "(no card)", -counts[s], s.lower()))

    return {
        "generated": f"{datetime.now():%Y-%m-%d}",
        "docs": docs,
        "refs": refs,
        "sources": [{"name": s, "count": counts[s]} for s in source_names],
        "stats": {
            "cards": len(carded),
            "sources": sum(1 for s in source_names if s != "(no card)"),
            "runtime": fmt_hm(sum(d["seconds"] for d in carded)),
            "runs": sum(d["runs"] for d in docs),
            "open": sum(1 for d in carded if d["status"] != "closed"),
        },
    }


BROWSER_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>media-reader — video cards</title>
<style>
:root{
  --paper:#faf8f4; --ink:#231f1a; --ink2:#6b6259; --ink3:#968c7e;
  --rule:#e2dbcf; --rule2:#efe9df; --hi:#f2ece1;
  --accent:#a4661e; --teal:#1a7d80;
  --ui:system-ui,-apple-system,"Segoe UI",sans-serif;
  --serif:Georgia,"Iowan Old Style","Source Serif 4",serif;
  --mono:ui-monospace,Menlo,Consolas,"DejaVu Sans Mono",monospace;
}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:400 15px/1.5 var(--ui);
     -webkit-text-size-adjust:100%}
a{color:var(--accent)}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}

/* ---- masthead ---- */
header.top{border-bottom:1px solid var(--rule);margin-bottom:22px}
.mast{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;padding:26px 0 4px}
.mast h1{margin:0;font:600 17px/1 var(--ui);letter-spacing:.14em;text-transform:uppercase}
.mast .stats{font:400 12px/1 var(--mono);color:var(--ink3)}
.refs{display:flex;gap:8px;flex-wrap:wrap;align-items:baseline;padding:12px 0 18px;
      font-size:13px;color:var(--ink3)}
.refs a{text-decoration:none;border-bottom:1px solid rgba(164,102,30,.32);padding-bottom:1px}
.refs a:hover{border-bottom-color:var(--accent)}
.refs .sep{color:var(--rule)}

/* ---- controls ---- */
.controls{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;
          padding-bottom:14px}
.sources{display:flex;gap:6px;flex-wrap:wrap;flex:1;min-width:0}
button.src{font:400 12.5px/1 var(--ui);padding:6px 11px;border:1px solid var(--rule);
           border-radius:3px;background:transparent;color:var(--ink2);cursor:pointer}
button.src:hover{border-color:#bfb5a4;color:var(--ink)}
button.src.on{background:var(--accent);border-color:var(--accent);color:var(--paper)}
button.src b{font-weight:400;opacity:.6;margin-left:5px;font-family:var(--mono);font-size:11px}
input#q{font:400 13px/1 var(--ui);padding:7px 10px;width:230px;color:var(--ink);
        border:1px solid var(--rule);border-radius:3px;background:#fff;outline:none}
input#q:focus{border-color:var(--accent)}

/* ---- table ---- */
table.index{width:100%;border-collapse:collapse;margin-bottom:60px}
.index th{position:sticky;top:0;z-index:1;background:var(--paper);text-align:left;
          font:600 10px/1 var(--ui);letter-spacing:.13em;text-transform:uppercase;
          color:var(--ink3);padding:10px 14px 9px 0;border-bottom:1px solid var(--rule);
          cursor:pointer;white-space:nowrap;user-select:none}
.index th:hover{color:var(--ink)}
.index th .car{opacity:.35;margin-left:4px;font-size:9px}
.index th.on{color:var(--accent)}
.index th.on .car{opacity:1}
.index td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule2);
          vertical-align:baseline}
.index th:last-child,.index td:last-child{padding-right:0}
.index tr:hover td{background:var(--hi)}
.num{text-align:right;font-family:var(--mono);font-size:12px;color:var(--ink3);
     white-space:nowrap}
td.src{font-size:12px;color:var(--ink2);white-space:nowrap}
td.ttl a{color:var(--ink);text-decoration:none;font-size:14.5px;line-height:1.35;
         border-bottom:1px solid transparent}
td.ttl a:hover{color:var(--accent);border-bottom-color:rgba(164,102,30,.4)}
td.ttl .vid{display:block;font:400 10.5px/1.5 var(--mono);color:var(--ink3);margin-top:3px}
.pill{display:inline-block;font:400 10px/1 var(--mono);letter-spacing:.06em;
      text-transform:uppercase;padding:3px 6px;border-radius:2px;
      background:#ece6da;color:var(--ink2)}
.pill.open{background:rgba(164,102,30,.13);color:#8a5416}
.pill.none{background:transparent;color:var(--ink3);border:1px solid var(--rule)}
tr.uncarded td.ttl a{color:var(--ink3);font-style:italic}
.empty{padding:44px 0 60px;color:var(--ink3);font-size:14px}

/* ---- document view ---- */
.docnav{display:flex;align-items:baseline;gap:16px;padding-bottom:20px;font-size:13px}
.docnav a{text-decoration:none}
.docnav .steps{margin-left:auto;display:flex;gap:14px}
.docnav .off{color:var(--ink3);opacity:.45}
.dochead{border-bottom:1px solid var(--rule);padding-bottom:18px;margin-bottom:26px}
.kicker{font:400 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
        color:var(--accent)}
.dochead h1{margin:11px 0 0;font:600 27px/1.25 var(--serif);max-width:30em}
.dmeta{margin-top:12px;font:400 12px/1.6 var(--mono);color:var(--ink3);
       display:flex;gap:14px;flex-wrap:wrap;align-items:baseline}
.dmeta .path{margin-left:auto}

.prose{max-width:44em;font:400 16.5px/1.62 var(--serif);color:#2b2620;
       padding-bottom:110px}
.prose h1{font:600 24px/1.25 var(--serif);margin:0 0 18px}
.prose h2{font:600 11px/1 var(--ui);letter-spacing:.16em;text-transform:uppercase;
          color:var(--ink3);margin:40px 0 15px;padding-top:19px;
          border-top:1px solid var(--rule2)}
.prose h2:first-child{margin-top:0;padding-top:0;border-top:0}
.prose h3{font:600 15px/1.35 var(--ui);color:#3d372e;margin:28px 0 10px}
.prose h2+p{font:400 13px/1.5 var(--ui);color:var(--ink3);margin:-7px 0 22px}
.prose p{margin:0 0 15px;text-wrap:pretty}
.prose ul,.prose ol{margin:0 0 15px;padding-left:21px}
.prose li{margin:0 0 8px}
.prose li>ul,.prose li>ol{margin:8px 0 0}
.prose strong{font-weight:700;color:#191510}
.prose strong.v{color:var(--teal)}
.prose strong.u{color:#96651f}
.prose em{color:var(--ink2)}
.prose code{font:400 .82em/1.4 var(--mono);background:#f1ece2;border:1px solid #e6dfd3;
            border-radius:2px;padding:0 4px;color:#7a4a12}
.prose a{text-decoration:none;border-bottom:1px solid rgba(164,102,30,.3)}
.prose a:hover{border-bottom-color:var(--accent)}
.prose .ref{font:400 .85em/1 var(--mono);color:var(--ink3)}
.prose hr{border:0;border-top:1px solid var(--rule);margin:26px 0}
.prose table{border-collapse:collapse;width:100%;margin:2px 0 24px;
             font:400 13px/1.45 var(--ui)}
.prose th{font:600 9.5px/1 var(--ui);letter-spacing:.12em;text-transform:uppercase;
          color:var(--ink3);text-align:left;padding:0 14px 8px 0;
          border-bottom:1px solid var(--rule);white-space:nowrap}
.prose td{padding:8px 14px 8px 0;border-bottom:1px solid var(--rule2);
          vertical-align:top;color:#3d372e}
.prose th:last-child,.prose td:last-child{padding-right:0}
.prose blockquote{margin:0 0 15px;padding-left:16px;border-left:2px solid var(--rule);
                  color:var(--ink2)}
.tablewrap{overflow-x:auto}

@media (max-width:820px){
  .wrap{padding:0 16px}
  .index td.up,.index th.up,.index td.rn,.index th.rn{display:none}
  input#q{width:100%}
}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="mast">
    <h1>media-reader</h1>
    <div class="stats" id="stats"></div>
  </div>
  <div class="refs" id="refs"></div>
</div></header>
<div class="wrap"><main id="app"></main></div>

<script>
"use strict";
const DATA = __DATA__;

const byKey = {};
for (const d of DATA.docs.concat(DATA.refs)) byKey[d.key] = d;

let state = { q: "", source: "", sort: "source", dir: 1 };

/* ------------------------------------------------------------ markdown --- */

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function slug(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

/* repo-relative links become routes in this page */
function hrefRoute(h) {
  let m = h.match(/^(?:\.\.\/)*dossiers\/([A-Za-z0-9_-]+)\//);
  if (m) return byKey["v:" + m[1]] ? "#/v/" + m[1] : null;
  m = h.match(/^playlists\/(.+\.md)$/);
  if (m) return byKey["p:" + m[1]] ? "#/p/" + m[1] : null;
  if (/^INDEX\.md$/.test(h)) return "#/index";
  return null;
}

function inline(s) {
  const codes = [];
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, (m, c) => { codes.push(c); return "@@C" + (codes.length - 1) + "@@"; });
  s = s.replace(/\[([^\]]*)\]\(([^)\s]+)\)/g, (m, t, h) => {
    h = h.replace(/&amp;/g, "&");
    if (/^https?:/.test(h)) return '<a href="' + h + '" target="_blank" rel="noopener">' + t + "</a>";
    if (h.charAt(0) === "#") return '<a href="#" class="jump" data-anchor="' + esc(h.slice(1)) + '">' + t + "</a>";
    const r = hrefRoute(h);
    return r ? '<a href="' + r + '">' + t + "</a>" : '<span class="ref">' + t + "</span>";
  });
  s = s.replace(/\*\*(Unverified[^*]*)\*\*/g, '<strong class="u">$1</strong>');
  s = s.replace(/\*\*(Verified[^*]*)\*\*/g, '<strong class="v">$1</strong>');
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  /* asterisks hugging their text; loose ones are transcribed screen glyphs */
  s = s.replace(/(^|[^*\w])\*([^\s*](?:[^*\n]*[^\s*])?)\*(?![\w*])/g, "$1<em>$2</em>");
  s = s.replace(/(^|[\s("“—])_([^_\n]+)_(?=$|[\s.,;:)"”!?—])/g, "$1<em>$2</em>");
  s = s.replace(/@@C(\d+)@@/g, (m, i) => "<code>" + codes[Number(i)] + "</code>");
  return s;
}

function cells(r) {
  return r.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(c => c.trim());
}

function tableBlock(rows) {
  const head = cells(rows[0]);
  const align = cells(rows[1]).map(a => /:$/.test(a) ? (/^:/.test(a) ? "center" : "right") : "left");
  let out = '<div class="tablewrap"><table><thead><tr>';
  head.forEach((h, i) => { out += '<th style="text-align:' + (align[i] || "left") + '">' + inline(h) + "</th>"; });
  out += "</tr></thead><tbody>";
  for (let r = 2; r < rows.length; r++) {
    const c = cells(rows[r]);
    out += "<tr>";
    head.forEach((_, j) => { out += '<td style="text-align:' + (align[j] || "left") + '">' + inline(c[j] || "") + "</td>"; });
    out += "</tr>";
  }
  return out + "</tbody></table></div>";
}

function listBlock(items) {
  const tag = items.length && items[0].ord ? "ol" : "ul";
  let out = "<" + tag + ">", open = false, started = false;
  for (const it of items) {
    if (it.depth > 0) {
      if (!open) { out += "<ul>"; open = true; }
      out += "<li>" + inline(it.text) + "</li>";
    } else {
      if (open) { out += "</ul>"; open = false; }
      if (started) out += "</li>";
      out += "<li>" + inline(it.text);
      started = true;
    }
  }
  if (open) out += "</ul>";
  if (started) out += "</li>";
  return out + "</" + tag + ">";
}

/* a line starting with "|" is only a table when a separator row follows */
function isTable(lines, i) {
  return /^\s*\|/.test(lines[i]) && i + 1 < lines.length &&
         /^\s*\|[\s:|-]+\|?\s*$/.test(lines[i + 1]);
}

function md(src) {
  const lines = String(src).split("\n"), out = [];
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (/^\s*$/.test(l)) { i++; continue; }

    const h = l.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      const lv = h[1].length;
      out.push("<h" + lv + ' id="h-' + slug(h[2]) + '">' + inline(h[2]) + "</h" + lv + ">");
      i++; continue;
    }
    if (/^\s*(-{3,}|_{3,}|\*{3,})\s*$/.test(l)) { out.push("<hr>"); i++; continue; }

    if (isTable(lines, i)) {
      const rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) { rows.push(lines[i]); i++; }
      out.push(tableBlock(rows));
      continue;
    }

    if (/^\s*(?:[-*]|\d+\.)\s+/.test(l)) {
      const items = [];
      while (i < lines.length) {
        const m = lines[i].match(/^(\s*)(?:[-*]|(\d+)\.)\s+(.*)$/);
        if (m) items.push({ depth: m[1].length >= 2 ? 1 : 0, ord: !!m[2], text: m[3] });
        else if (items.length && /^\s+\S/.test(lines[i])) items[items.length - 1].text += " " + lines[i].trim();
        else break;
        i++;
      }
      out.push(listBlock(items));
      continue;
    }

    if (/^\s*>/.test(l)) {
      const q = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) { q.push(lines[i].replace(/^\s*>\s?/, "")); i++; }
      out.push("<blockquote>" + md(q.join("\n")) + "</blockquote>");
      continue;
    }

    /* always consume the opening line, so this loop can never stall */
    const para = [lines[i].trim()];
    i++;
    while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^#{1,4}\s/.test(lines[i]) &&
           !/^\s*(?:[-*]|\d+\.)\s/.test(lines[i]) && !isTable(lines, i) && !/^\s*>/.test(lines[i])) {
      para.push(lines[i].trim()); i++;
    }
    out.push("<p>" + inline(para.join(" ")) + "</p>");
  }
  return out.join("");
}

/* ---------------------------------------------------------------- views --- */

const app = document.getElementById("app");

function visible() {
  const q = state.q.trim().toLowerCase();
  let rows = DATA.docs.filter(d =>
    (!state.source || d.source === state.source) &&
    (!q || (d.title + " " + d.channel + " " + d.id).toLowerCase().includes(q)));

  const dir = state.dir;
  const cmp = {
    source:  (a, b) => (a.source || "~").localeCompare(b.source || "~") ||
                       (a.pos || 99) - (b.pos || 99) ||
                       a.uploaded.localeCompare(b.uploaded),
    pos:     (a, b) => (a.pos || 99) - (b.pos || 99),
    title:   (a, b) => a.title.localeCompare(b.title),
    uploaded:(a, b) => a.uploaded.localeCompare(b.uploaded),
    seconds: (a, b) => a.seconds - b.seconds,
    runs:    (a, b) => a.runs - b.runs,
    status:  (a, b) => a.status.localeCompare(b.status),
  }[state.sort];
  rows.sort((a, b) => cmp(a, b) * dir);
  return rows;
}

const COLS = [
  { key: "source",   label: "Source",  cls: "src" },
  { key: "pos",      label: "#",       cls: "num" },
  { key: "title",    label: "Title",   cls: "ttl" },
  { key: "uploaded", label: "Uploaded",cls: "up" },
  { key: "seconds",  label: "Length",  cls: "num" },
  { key: "runs",     label: "Runs",    cls: "num rn" },
  { key: "status",   label: "Status",  cls: "st" },
];

function renderTable() {
  const rows = visible();

  let h = '<div class="controls"><div class="sources">';
  h += '<button class="src' + (state.source === "" ? " on" : "") + '" data-src="">All' +
       "<b>" + DATA.docs.length + "</b></button>";
  for (const s of DATA.sources) {
    h += '<button class="src' + (state.source === s.name ? " on" : "") + '" data-src="' +
         esc(s.name) + '">' + esc(s.name) + "<b>" + s.count + "</b></button>";
  }
  h += '</div><input id="q" type="search" placeholder="Filter titles…" value="' +
       esc(state.q) + '"></div>';

  h += '<table class="index"><thead><tr>';
  for (const c of COLS) {
    const on = state.sort === c.key;
    h += '<th class="' + c.cls + (on ? " on" : "") + '" data-sort="' + c.key + '">' + c.label +
         '<span class="car">' + (on ? (state.dir > 0 ? "▲" : "▼") : "△") + "</span></th>";
  }
  h += "</tr></thead><tbody>";

  for (const d of rows) {
    const uncarded = d.status === "no card";
    h += '<tr class="' + (uncarded ? "uncarded" : "") + '">' +
      '<td class="src">' + esc(d.source || "—") + "</td>" +
      '<td class="num">' + (d.pos || "·") + "</td>" +
      '<td class="ttl"><a href="#/v/' + d.id + '">' + esc(d.title) +
        '<span class="vid">' + d.id + (d.playlist ? " · " + d.playlist : "") + "</span></a></td>" +
      '<td class="num up">' + (d.uploaded || "—") + "</td>" +
      '<td class="num">' + (d.duration || "—") + "</td>" +
      '<td class="num rn">' + d.runs + "</td>" +
      '<td class="st"><span class="pill ' +
        (uncarded ? "none" : d.status === "closed" ? "" : "open") + '">' + esc(d.status) + "</span></td>" +
      "</tr>";
  }
  h += "</tbody></table>";
  if (!rows.length) h += '<div class="empty">Nothing matches that filter.</div>';

  app.innerHTML = h;
  const q = document.getElementById("q");
  q.addEventListener("input", e => {
    state.q = e.target.value;
    const at = e.target.selectionStart;
    renderTable();
    const nq = document.getElementById("q");
    nq.focus(); nq.setSelectionRange(at, at);
  });
  app.querySelectorAll("button.src").forEach(b =>
    b.addEventListener("click", () => { state.source = b.dataset.src; renderTable(); }));
  app.querySelectorAll("th[data-sort]").forEach(th =>
    th.addEventListener("click", () => {
      const k = th.dataset.sort;
      if (state.sort === k) state.dir = -state.dir;
      else { state.sort = k; state.dir = 1; }
      renderTable();
    }));
  document.title = "media-reader — video cards";
}

function renderDoc(key) {
  const d = byKey[key];
  if (!d) { location.hash = "#/"; return; }

  let h = '<div class="docnav"><a href="#/">← All cards</a>';
  if (d.kind === "video") {
    const sibs = visible();
    const at = sibs.findIndex(x => x.key === key);
    const prev = at > 0 ? sibs[at - 1] : null;
    const next = at >= 0 && at < sibs.length - 1 ? sibs[at + 1] : null;
    h += '<div class="steps">' +
      (prev ? '<a href="#/v/' + prev.id + '">‹ previous</a>' : '<span class="off">‹ previous</span>') +
      (next ? '<a href="#/v/' + next.id + '">next ›</a>' : '<span class="off">next ›</span>') +
      "</div>";
  }
  h += "</div>";

  const bits = [];
  if (d.kind === "video") {
    if (d.pos) bits.push("#" + d.pos + " in playlist");
    if (d.uploaded) bits.push(d.uploaded);
    if (d.duration) bits.push(d.duration);
    bits.push(d.status);
    if (d.status !== "no card") bits.push(d.runs + " runs");
  }

  h += '<div class="dochead"><div class="kicker">' +
    esc(d.kind === "video" ? (d.channel || d.id)
        : d.kind === "index" ? "generated index" : "playlist synthesis") +
    "</div><h1>" + esc(d.title) + "</h1><div class=\"dmeta\">";
  if (bits.length) h += "<span>" + esc(bits.join("  ·  ")) + "</span>";
  if (d.subtitle) h += "<span>" + esc(d.subtitle) + "</span>";
  if (d.url) h += '<a href="' + d.url + '" target="_blank" rel="noopener">watch on YouTube</a>';
  h += '<span class="path">' + esc(d.file) + "</span></div></div>";

  h += '<div class="prose">' + md(d.body) + "</div>";
  app.innerHTML = h;

  app.querySelectorAll("a.jump").forEach(a =>
    a.addEventListener("click", e => {
      e.preventDefault();
      const t = document.getElementById("h-" + a.dataset.anchor);
      if (t) t.scrollIntoView({ behavior: "smooth", block: "start" });
    }));

  document.title = d.title + " — media-reader";
  window.scrollTo(0, 0);
}

function route() {
  const h = location.hash.replace(/^#/, "");
  let m = h.match(/^\/v\/(.+)$/);
  if (m) return renderDoc("v:" + m[1]);
  m = h.match(/^\/p\/(.+)$/);
  if (m) return renderDoc("p:" + m[1]);
  if (h === "/index") return renderDoc("index");
  renderTable();
}

/* ---------------------------------------------------------------- boot --- */

const st = DATA.stats;
document.getElementById("stats").textContent =
  st.cards + " cards · " + st.sources + " sources · " + st.runtime +
  " · " + st.runs + " runs" + (st.open ? " · " + st.open + " open" : "") +
  " · generated " + DATA.generated;

document.getElementById("refs").innerHTML =
  DATA.refs.map(r => '<a href="#/' + (r.kind === "index" ? "index" : "p/" + r.id) + '">' +
                     esc(r.title) + "</a>").join('<span class="sep">/</span>');

window.addEventListener("hashchange", route);
route();
</script>
</body>
</html>
"""


def render_browser(payload):
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    blob = blob.replace("</", "<\\/")          # cannot close the <script>
    return BROWSER_TEMPLATE.replace("__DATA__", blob)


def cmd_browse(args):
    payload = browse_documents()
    html = render_browser(payload)
    out = Path(args.out) if args.out else BROWSER_PATH
    out.write_text(html)
    st = payload["stats"]
    print(f"{out.name}: {st['cards']} cards, {len(payload['refs'])} reference docs, "
          f"{st['sources']} sources — {len(html):,} bytes")
