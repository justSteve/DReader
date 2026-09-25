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

FILES = [
    REPO_ROOT / "media-reader" / "mread.py",
    REPO_ROOT / "media-reader" / "reader.template.html",
]


def test_no_stale_videos_route():
    for path in FILES:
        text = path.read_text()
        assert "videos\\/" not in text, (
            f"{path.relative_to(REPO_ROOT)} still contains the JS-escaped "
            "route pattern 'videos\\/' — the dossiers/ rename (dr-dqm, "
            "2026-09-25) missed a route regex embedded in a template string"
        )
