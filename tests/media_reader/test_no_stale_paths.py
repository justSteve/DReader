"""Pins dr-dqm.1's Task 6 regression: the output oracle (compare_outputs.py)
normalises dossiers/ -> videos/ before diffing, so a stale `videos/` route
regex embedded in JS template strings is invisible to it — the rendered
browser.html and reader.html looked byte-identical to baseline while every
card link in the browser's index view was silently dead (hrefRoute in
BROWSER_TEMPLATE, and its counterpart in reader.template.html, still matched
only `^videos\\/...`). This test reads the source files directly, where the
oracle cannot mask it."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Every module of the tool (BROWSER_TEMPLATE moved to corpus.py in Task 7, so
# a scan of mread.py alone would pass vacuously), minus the yta.py shim.
TOOL_DIR = REPO_ROOT / "media-reader"
FILES = sorted(p for p in TOOL_DIR.glob("*.py") if p.name != "yta.py") + [
    TOOL_DIR / "reader.template.html",
]


def test_no_stale_videos_route():
    for path in FILES:
        text = path.read_text()
        assert "videos\\/" not in text, (
            f"{path.relative_to(REPO_ROOT)} still contains the JS-escaped "
            "route pattern 'videos\\/' — the dossiers/ rename (dr-dqm, "
            "2026-09-25) missed a route regex embedded in a template string"
        )
