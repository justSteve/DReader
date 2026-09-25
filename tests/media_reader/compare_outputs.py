#!/usr/bin/env python3
"""Refactor oracle for dr-dqm: regenerate every derived output of the media
tool and compare it with a baseline taken before the refactor began.

  .venv/bin/python tests/media_reader/compare_outputs.py save    # once, Task 1
  .venv/bin/python tests/media_reader/compare_outputs.py check   # after every task

It finds the tool wherever it currently lives (yt-analyst/yta.py before
Task 5, media-reader/mread.py after) and runs it with that tool's own venv.
The renames this refactor makes on purpose are normalised away on both sides,
so any difference that survives is one nobody intended. Exit 1 on any diff.
"""
import difflib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / ".refactor-baseline"
CANDIDATES = [("media-reader", "mread.py"), ("yt-analyst", "yta.py")]
NORMALISE = [
    (r'"generated": "[^"]*"', '"generated": "X"'),
    (r"generated \d{4}-\d{2}-\d{2}", "generated X"),
    (r"\bdossiers/", "videos/"),
    (r"mread\.py", "yta.py"),
    (r"media-reader", "yt-analyst"),
    (r'"schema_version": 2', '"schema_version": 1'),
]


def tool():
    for d, entry in CANDIDATES:
        if (REPO / d / entry).exists():
            return REPO / d, entry
    sys.exit("no media tool found")


def generate(out):
    tdir, entry = tool()
    py = str(tdir / ".venv" / "bin" / "python")
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "INDEX.md", "w") as f:
        subprocess.run([py, entry, "index", "--stdout"], cwd=tdir, stdout=f, check=True)
    subprocess.run([py, entry, "export", "--out", str(out / "export.json")],
                   cwd=tdir, check=True, stderr=subprocess.DEVNULL)
    subprocess.run([py, entry, "browse", "--out", str(out / "browser.html")],
                   cwd=tdir, check=True, stdout=subprocess.DEVNULL)
    subprocess.run([py, "build_corpus.py", "--out", str(out / "corpus.json")],
                   cwd=tdir, check=True, stdout=subprocess.DEVNULL)


def norm(text):
    for pat, rep in NORMALISE:
        text = re.sub(pat, rep, text)
    return text.splitlines(keepends=True)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "save":
        generate(BASE)
        print(f"baseline saved to {BASE}")
        return
    now = REPO / ".refactor-now"
    generate(now)
    bad = 0
    for name in ("INDEX.md", "export.json", "browser.html", "corpus.json"):
        a = norm((BASE / name).read_text())
        b = norm((now / name).read_text())
        diff = list(difflib.unified_diff(a, b, f"baseline/{name}", f"now/{name}", n=1))
        if diff:
            bad += 1
            sys.stdout.writelines(diff[:80])
        print(f"{name}: {'DIFFERS' if diff else 'identical'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
