#!/usr/bin/env python3
"""Assemble reader.html — the Ledger reading interface — from reader.template.html
and corpus.json. The page is self-contained: the corpus and each video's cover
image (videos/<id>/thumb.jpg, from fetch_thumbs.py) ride inline, because the
published page cannot load anything from the network. Rerun after
`python3 build_corpus.py`.

Scope decisions that belong to the reader, not the corpus, live here:
EXCLUDE drops videos Steve does not want shown (see EDITS.md); cards whose
header status is `shelved` are dropped the same way.

  python3 build_reader.py [--out reader.html]
"""
import base64, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDE = {
    "yWO8hVpRXeY",   # the live DAX trade — not SPX/ES (EDITS.md, 2026-09-07)
}


def scope(corpus):
    cards = [c for c in corpus["cards"]
             if c["id"] not in EXCLUDE
             and (c.get("status") or "").split()[:1] != ["shelved"]]
    ids = {c["id"] for c in cards}
    edges = [e for e in corpus["edges"] if e["from"] in ids and e["to"] in ids]
    for c in cards:
        c["links_in"] = [i for i in c["links_in"] if i in ids]
        c["links_out"] = [i for i in c["links_out"] if i in ids]
        if c["read"]:
            c["read"]["links_out"] = [i for i in c["read"]["links_out"] if i in ids]
        thumb = ROOT / "videos" / c["id"] / "thumb.jpg"
        c["thumb"] = base64.b64encode(thumb.read_bytes()).decode("ascii") if thumb.exists() else None
    channels = [{"name": g["name"], "cards": [i for i in g["cards"] if i in ids]} for g in corpus["channels"]]
    channels = [g for g in channels if g["cards"]]
    counts = dict(corpus["counts"])
    counts.update({
        "cards": len(cards), "edges": len(edges), "channels": len(channels),
        "graded": sum(1 for c in cards if c["grades"]),
        "reads": sum(1 for c in cards if c["read"]),
        "asides": sum(len(c["read"]["asides"]) for c in cards if c["read"]),
        "corrections": sum(c["corrections"] for c in cards),
        "runs": sum(c["runs"] for c in cards),
        "excluded": len(corpus["cards"]) - len(cards),
    })
    return {**corpus, "cards": cards, "edges": edges, "channels": channels, "counts": counts}


if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "reader.html"
    corpus = scope(json.loads((ROOT / "corpus.json").read_text()))
    blob = json.dumps(corpus, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (ROOT / "reader.template.html").read_text().replace("__DATA__", blob, 1)
    out.write_text(html)
    c = corpus["counts"]
    thumbs = sum(1 for x in corpus["cards"] if x["thumb"])
    print(f"{out.name}: {c['cards']} cards ({c['excluded']} excluded), {c['reads']} reads, "
          f"{thumbs} covers, {out.stat().st_size/1024:.0f} KB")
