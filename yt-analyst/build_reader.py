#!/usr/bin/env python3
"""Assemble reader.html — the Ledger reading interface — from reader.template.html
and corpus.json. The page is self-contained (the corpus rides inline) and is
published as an Artifact; rerun after `python3 build_corpus.py`.

  python3 build_reader.py [--out reader.html]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "reader.html"
    corpus = json.loads((ROOT / "corpus.json").read_text())
    # compact, and safe inside a <script> element
    blob = json.dumps(corpus, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (ROOT / "reader.template.html").read_text().replace("__DATA__", blob, 1)
    out.write_text(html)
    c = corpus["counts"]
    print(f"{out.name}: {c['cards']} cards, {c['reads']} reads, {out.stat().st_size/1024:.0f} KB")
