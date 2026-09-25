# media-reader, Plan A — foundation: shared core, rename, split, source seam

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `yt-analyst/yta.py` into `media-reader/mread.py`, a media-ingestion tool with one seam where a new source kind plugs in. It shares one Gemini core with `discord-reader/dread.py`. Every output the current 58-card corpus produces stays byte-identical, apart from the renames made on purpose.

**Bead:** dr-dqm (epic). This plan is dr-dqm.1. Plan B (audio, image and document sources) is dr-dqm.2 and starts after this one lands.

**Architecture:** A new package, `dreader_core/`, at the repo root holds everything the two tools duplicate today: credentials, Gemini retry and fallback, Files-API upload, and run archiving. Each tool puts the repo root on `sys.path` and imports it. The yta monolith (1,943 lines) is renamed, and its dossier directory `videos/` becomes `dossiers/`. It is then split by responsibility into `sources / prompts / perceive / verify / corpus` modules behind a thin CLI. A `Source` record (`kind`, `id`, `url`, `path`, `mime`, `card`) replaces the `(vid, url, path, card)` tuple, which is the seam Plan B fills.

**Tech Stack:** Python 3.12, google-genai 2.20.0, httpx 0.28.1, yt-dlp, ffmpeg/ffprobe, pytest 9 (repo-root `.venv`).

---

## Rulings this plan implements (Steve, 2026-09-18 and 2026-09-25)

- 09-18 (session 2f9ef07d): *"the name YouTube-Analyst is too YouTube specific … this repository manages media ingestion … it is a tool … not a Z agent, but is a service to."*
- 09-25: name **`media-reader/`** (`mread.py`, next to `dread.py`). **discord-reader shares the core only.** It keeps its directory, private captures and doctrine. **In scope:** audio/podcasts, screenshots/images, documents/PDFs/email. Those go in Plan B.

## Why the shared core is not cosmetic

The two scripts already disagree on four things a fix was supposed to change in both:

| Behaviour | yta.py | dread.py |
|---|---|---|
| Fallback model | `gemini-3.6-flash` (dr-9qo) | `gemini-2.5-flash`, **retired 2026-09-06, now 404s** |
| httpx transport errors ("Server disconnected") | retried like a 503 (dr-8qq.13) | crash |
| Empty reply (`resp.text is None`) | diagnosed (dr-08s.9) | `TypeError` in `json.loads` |
| Two runs in the same second | unique run dirs (dr-8qq.11) | second run overwrites the first |

`tests/credential_loading/test_load_env.py` says *"the loader is duplicated between them by design. Every test here runs against both."* That design held for the loader and failed for everything else. After this plan there is one copy, and a test fails if either tool grows its own again.

## Hazards (read before any task)

- **Freeze card edits while this plan runs.** Task 1 snapshots every derived output and later tasks diff against that snapshot. A card edited mid-plan shows up as a false regression. If one is unavoidable, rerun `compare_outputs.py save` right after it, before the next task.
- **Venvs do not move.** `yt-analyst/.venv/bin/*` hard-code `/root/projects/DReader/yt-analyst/.venv/bin/python3`. Task 5 recreates the venv from `requirements.txt`. It never moves it.
- **`grep` here is a Claude Code shim** (`.claude/rules/shell-shim-hazards.md`). It skips gitignored files. The completeness sweeps below use `/usr/bin/grep` on purpose.
- **Gemini calls cost money.** Only Task 4 step 7 and Task 8 step 7 make live calls, and both use a 30-second clipped window.
- **Beads first.** Reference `dr-dqm.1` in every commit: `[dr-dqm.1] …`.

## File map

| Path | Status | Responsibility |
|---|---|---|
| `dreader_core/__init__.py` | create | package marker |
| `dreader_core/creds.py` | create | vault/env loading, `require_key`, the `env` report |
| `dreader_core/gemini.py` | create | model constants, retry and fallback, reply parsing, media-resolution config, SDK quieting |
| `dreader_core/uploads.py` | create | Files-API upload, with and without the 48 h handle cache |
| `dreader_core/runs.py` | create | unique run dirs, run-log append, `MM:SS` parse/format |
| `tests/conftest.py` | create | puts repo root and `media-reader/` on `sys.path` |
| `tests/dreader_core/test_*.py` | create | unit tests for the core |
| `tests/credential_loading/test_load_env.py` | rewrite | same regression tests, now against `dreader_core.creds` |
| `tests/test_tools_delegate.py` | create | pins that neither tool re-grows a private copy |
| `tests/media_reader/compare_outputs.py` | create | the refactor oracle (snapshot + diff) |
| `tests/media_reader/test_sources.py` | create | source resolution and kind detection |
| `requirements-test.txt` | create | what the root test venv needs |
| `yt-analyst/` → `media-reader/` | rename | Task 5 |
| `media-reader/yta.py` → `mread.py` | rename | Task 5; `yta.py` returns as a forwarding shim |
| `media-reader/videos/` → `dossiers/` | rename | Task 6 |
| `media-reader/{sources,prompts,perceive,verify,corpus}.py` | create | Task 7 split, Task 8 seam |
| `discord-reader/dread.py` | modify | imports the core, drops its copies |
| `docs/retired/REGISTER.md` | modify | the rename's invalidated premises |
| `.gitleaks.toml` | modify | allowlist paths follow the rename |

---

### Task 1: Baseline, oracle, and requirements

**Files:**
- Create: `tests/media_reader/compare_outputs.py`
- Create: `requirements-test.txt`
- Create: `yt-analyst/requirements.txt`, `discord-reader/requirements.txt`
- Modify: `.gitignore` (root)

- [ ] **Step 1: Pin each tool's dependencies before anything moves**

```bash
cd /root/projects/DReader
yt-analyst/.venv/bin/pip freeze > yt-analyst/requirements.txt
discord-reader/.venv/bin/pip freeze > discord-reader/requirements.txt
/usr/bin/grep -E '^(google-genai|httpx|yt-dlp)==' yt-analyst/requirements.txt
```
Expected: three lines, `google-genai==2.20.0`, `httpx==0.28.1`, `yt-dlp==2026.8.19`.

- [ ] **Step 2: Give the root test venv what the core tests import**

Create `requirements-test.txt`:
```
pytest==9.0.3
google-genai==2.20.0
httpx==0.28.1
```
Run: `.venv/bin/pip install -r requirements-test.txt`
Expected: `Successfully installed google-genai-2.20.0 …` (pytest already satisfied).

- [ ] **Step 3: Write the oracle**

Create `tests/media_reader/compare_outputs.py`:
```python
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
```

- [ ] **Step 4: Ignore the snapshot directories**

Append to the root `.gitignore`:
```
# dr-dqm refactor oracle — derived outputs, regenerated on demand
.refactor-baseline/
.refactor-now/
```

- [ ] **Step 5: Take the baseline and prove the oracle is quiet on an unchanged tree**

```bash
.venv/bin/python tests/media_reader/compare_outputs.py save
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: `baseline saved to …/.refactor-baseline`, then four lines ending `identical`, exit 0.

- [ ] **Step 6: Prove the oracle can fail**

```bash
cp yt-analyst/videos/IUWvHVout94/CARD.md /tmp/card.bak
sed -i '0,/\*\*Status:\*\* closed/s//**Status:** open/' yt-analyst/videos/IUWvHVout94/CARD.md
.venv/bin/python tests/media_reader/compare_outputs.py check; echo "exit=$?"
cp /tmp/card.bak yt-analyst/videos/IUWvHVout94/CARD.md
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: the first check prints `INDEX.md: DIFFERS` (and others) and `exit=1`. The second prints four `identical`.

- [ ] **Step 7: Commit**

```bash
git add requirements-test.txt yt-analyst/requirements.txt discord-reader/requirements.txt \
        tests/media_reader/compare_outputs.py .gitignore
git commit -m "[dr-dqm.1] Refactor oracle and pinned requirements before media-reader work"
```

---

### Task 2: `dreader_core.creds` — one credential loader

**Files:**
- Create: `dreader_core/__init__.py`, `dreader_core/creds.py`, `tests/conftest.py`
- Rewrite: `tests/credential_loading/test_load_env.py`
- Create: `tests/test_tools_delegate.py`
- Modify: `yt-analyst/yta.py` (delete `parse_env_file`, `secrets_path`, `load_env`, `require_key`, the body of `cmd_env`, constants `SECRETS_POINTER DEFAULT_SECRETS_PATH SECRET_NAMES MODELS_URL`)
- Modify: `discord-reader/dread.py` (same deletions)

- [ ] **Step 1: Path setup for every test**

Create `tests/conftest.py`:
```python
"""Put the repo root (for dreader_core) and the media tool's directory (for
its modules, from Task 7 on) on sys.path. The tools do the same for
themselves at import time, so tests and tools resolve the same module objects."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for p in (REPO_ROOT, REPO_ROOT / "media-reader"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
```

- [ ] **Step 2: Rewrite the credential tests against the core**

Replace `tests/credential_loading/test_load_env.py` entirely:
```python
"""Credential loading — the 2026-09-05 regression [co-yuyh9].

The credential sweep moved secret values into /home/vault/<project>/env, and
every shell already running on this box kept a dead April GEMINI_API_KEY. Both
tools loaded their env with ``os.environ.setdefault``, so the dead key won and
every Gemini call came back ``API key not valid``. These tests pin the
direction that fixes it: a value from a file overwrites the environment.

Until 2026-09-25 the loader was duplicated in yta.py and dread.py and every
test ran against both. It now lives once, in dreader_core.creds [dr-dqm.1];
tests/test_tools_delegate.py pins that neither tool grows a copy back.

Run: .venv/bin/pytest tests -q
"""
import os
from pathlib import Path

import pytest

from dreader_core import creds


@pytest.fixture(autouse=True)
def pristine_environ():
    before = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(before)


def write_env(path, text, mode=0o600):
    path.write_text(text)
    path.chmod(mode)
    return path


# ─── parse_env_file ──────────────────────────────────────────────────────────

def test_parse_handles_export_quotes_comments_and_junk(tmp_path):
    p = write_env(tmp_path / "env", "\n".join([
        "# a comment", "", "PLAIN=one", "export EXPORTED=two", 'QUOTED="three"',
        "SINGLE='four'", "  SPACED  =  five  ", "no_equals_sign_here", "EMPTY=",
        "URL=https://example.com/a?b=c",
    ]))
    assert creds.parse_env_file(p) == {
        "PLAIN": "one", "EXPORTED": "two", "QUOTED": "three", "SINGLE": "four",
        "SPACED": "five", "EMPTY": "", "URL": "https://example.com/a?b=c",
    }


def test_parse_later_line_wins(tmp_path):
    p = write_env(tmp_path / "env", "K=first\nK=second\n")
    assert creds.parse_env_file(p)["K"] == "second"


# ─── secrets_path ────────────────────────────────────────────────────────────

def test_pointer_names_the_file(tmp_path, monkeypatch):
    p = write_env(tmp_path / "env", "K=v\n")
    monkeypatch.setenv(creds.SECRETS_POINTER, str(p))
    assert creds.secrets_path() == (p, True)


def test_default_used_when_present_and_no_pointer(tmp_path, monkeypatch):
    p = write_env(tmp_path / "env", "K=v\n")
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", p)
    assert creds.secrets_path() == (p, False)


def test_no_vault_at_all(tmp_path, monkeypatch):
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    assert creds.secrets_path() == (None, False)


def test_the_vault_file_is_where_the_estate_says():
    assert creds.DEFAULT_SECRETS_PATH == Path("/home/vault/DReader/env")
    assert creds.SECRETS_POINTER == "DREADER_SECRETS_FILE"


# ─── load_env: the regression ────────────────────────────────────────────────

def test_vault_beats_a_stale_exported_key(tmp_path, monkeypatch):
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setenv("GEMINI_API_KEY", "dead-april-key")
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    creds.load_env(tmp_path / "no-tree")
    assert os.environ["GEMINI_API_KEY"] == "live-key"


def test_ambient_google_api_key_is_evicted(tmp_path, monkeypatch):
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setenv("GOOGLE_API_KEY", "some-other-google-key")
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    creds.load_env(tmp_path / "no-tree")
    assert "GOOGLE_API_KEY" not in os.environ


def test_secret_in_the_tree_is_refused_and_reported(tmp_path, monkeypatch, capsys):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_env(tree / ".env", "GEMINI_API_KEY=key-in-the-tree\nSETTING=kept\n")
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    creds.load_env(tree)
    assert os.environ["GEMINI_API_KEY"] == "live-key"
    assert os.environ["SETTING"] == "kept"
    assert "GEMINI_API_KEY ignored" in capsys.readouterr().err


def test_env_file_settings_beat_the_environment(tmp_path, monkeypatch):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_env(tree / ".env", "SETTING=from-file\n")
    monkeypatch.setenv("SETTING", "from-shell")
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    creds.load_env(tree)
    assert os.environ["SETTING"] == "from-file"


def test_pointer_at_a_missing_file_stops_the_run(tmp_path, monkeypatch):
    monkeypatch.setenv(creds.SECRETS_POINTER, str(tmp_path / "absent"))
    with pytest.raises(SystemExit) as e:
        creds.load_env(tmp_path / "no-tree")
    assert "does not exist" in str(e.value)


def test_loose_vault_permissions_are_reported_not_fatal(tmp_path, monkeypatch, capsys):
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n", mode=0o644)
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    creds.load_env(tmp_path / "no-tree")
    assert os.environ["GEMINI_API_KEY"] == "live-key"
    assert "should be 0600" in capsys.readouterr().err


# ─── require_key ─────────────────────────────────────────────────────────────

def test_missing_key_names_the_vault_file_and_the_tool(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv(creds.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(creds, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    with pytest.raises(SystemExit) as e:
        creds.require_key("mread.py")
    msg = str(e.value)
    assert str(tmp_path / "absent") in msg
    assert "`mread.py env` shows what was found" in msg


def test_present_key_passes_quietly(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "anything")
    assert creds.require_key("mread.py") is None
```

- [ ] **Step 3: Write the delegation test**

Create `tests/test_tools_delegate.py`:
```python
"""Neither tool may carry a private copy of what dreader_core holds [dr-dqm.1].

The copies drifted before: dread.py kept a retired fallback model, no
transport-error retry and no empty-reply guard for weeks after yta.py fixed
all three. This test fails the moment a copy grows back."""
import importlib.util
import sys
from pathlib import Path

import pytest

import dreader_core.creds

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "media": [REPO_ROOT / "media-reader" / "mread.py", REPO_ROOT / "yt-analyst" / "yta.py"],
    "dread": [REPO_ROOT / "discord-reader" / "dread.py"],
}
PRIVATE_COPIES = ["parse_env_file", "secrets_path", "load_env", "require_key",
                  "SECRETS_POINTER", "DEFAULT_SECRETS_PATH"]


@pytest.fixture(params=sorted(TOOLS), ids=sorted(TOOLS))
def tool(request):
    path = next((p for p in TOOLS[request.param] if p.exists()), None)
    assert path, f"no script found among {TOOLS[request.param]}"
    name = f"{request.param}_under_test"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    yield mod
    del sys.modules[name]


@pytest.mark.parametrize("name", PRIVATE_COPIES)
def test_no_private_copy(tool, name):
    assert not hasattr(tool, name), f"{tool.__name__} defines its own {name}"


def test_uses_the_shared_creds(tool):
    assert tool.creds is dreader_core.creds
```

- [ ] **Step 4: Run the tests and watch them fail**

Run: `.venv/bin/pytest tests -q`
Expected: collection error, `ModuleNotFoundError: No module named 'dreader_core'`.

- [ ] **Step 5: Create the core module**

Create `dreader_core/__init__.py`:
```python
"""Shared machinery for DReader's two collectors, media-reader and
discord-reader: credentials, Gemini calls, uploads, run archives [dr-dqm]."""
```

Create `dreader_core/creds.py`. The bodies of `parse_env_file`, `secrets_path` and `load_env` are copied **verbatim** from `yt-analyst/yta.py` (keep their docstrings), with two changes. `load_env` takes `tool_dir`, where it used `SCRIPT_DIR`, and `require_key` takes the tool's name:
```python
"""The vault: where the secret value lives, and how a tool loads it.

Secret values live in one file outside every project tree, mode 0600; the
repo holds a pointer at most. Set DREADER_SECRETS_FILE to read a different
file — that is the only supported override, and it must exist."""
import hashlib
import json
import os
import sys
from pathlib import Path

SECRETS_POINTER = "DREADER_SECRETS_FILE"
DEFAULT_SECRETS_PATH = Path("/home/vault/DReader/env")
SECRET_NAMES = ("GEMINI_API_KEY",)
MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1"


def parse_env_file(path):
    # verbatim from yta.py
    ...


def secrets_path():
    # verbatim from yta.py
    ...


def load_env(tool_dir):
    """<yta.py's docstring, plus:> ``tool_dir`` is the directory whose ``.env``
    holds the tool's non-secret settings (DREAD_CAPTURE_DIR, for one)."""
    values = {}
    env_path = Path(tool_dir) / ".env"
    # … rest verbatim from yta.py's load_env …


def require_key(tool):
    """Exit with the one instruction that fixes it, naming the vault file."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    path, _ = secrets_path()
    where = path or DEFAULT_SECRETS_PATH
    sys.exit(f"GEMINI_API_KEY not set: add the line to {where} (mode 0600), "
             f"or point {SECRETS_POINTER} at the vault file that holds it. "
             f"`{tool} env` shows what was found.")


def report_env(tool_dir, tool, no_check):
    """Say where the credential came from and whether Google still accepts it.
    Never prints the value — length and a sha256 prefix are enough to tell two
    keys apart, which is the question this answers."""
    import urllib.error
    import urllib.request

    path, explicit = secrets_path()
    origin = f" (named by {SECRETS_POINTER})" if explicit else ""
    print(f"vault file : {path if path else '(none found)'}{origin}")
    local = Path(tool_dir) / ".env"
    print(f"local .env : {local if local.exists() else '(none — correct)'}")

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        require_key(tool)
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    print(f"credential : GEMINI_API_KEY, {len(key)} chars, sha256:{digest}")

    if no_check:
        return
    req = urllib.request.Request(MODELS_URL, headers={"x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"live check : HTTP {r.status} — the key authenticates")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail)["error"]["message"]
        except Exception:
            detail = detail[:200]
        sys.exit(f"live check : HTTP {e.code} — {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"live check : no answer from Google — {e.reason}")
```
(The `# verbatim` markers mean *paste the function body from yta.py lines 146–215 here*. The code is not duplicated in this plan because it moves unchanged.)

- [ ] **Step 6: Point both tools at it**

In `yt-analyst/yta.py`, directly under `SCRIPT_DIR = …`:
```python
# The shared core lives at the repo root [dr-dqm].
sys.path.insert(0, str(SCRIPT_DIR.parent))
from dreader_core import creds  # noqa: E402
```
Delete from yta.py: `SECRETS_POINTER`, `DEFAULT_SECRETS_PATH`, `SECRET_NAMES`, `MODELS_URL`, and the functions `parse_env_file`, `secrets_path`, `load_env`, `require_key`. Then make these replacements:
- every `require_key()` call → `creds.require_key("yta.py")`
- in `main()`: `load_env()` → `creds.load_env(SCRIPT_DIR)`
- `cmd_env` body → `creds.report_env(SCRIPT_DIR, "yta.py", args.no_check)`
- remove `import hashlib` if nothing else uses it (`/usr/bin/grep -n hashlib yt-analyst/yta.py`)

Do the same in `discord-reader/dread.py`, with `"dread.py"` as the tool name.

- [ ] **Step 7: Run the tests**

Run: `.venv/bin/pytest tests -q`
Expected: all pass. The delegation tests are 7 checks × 2 tools = 14.

- [ ] **Step 8: Check the live paths are unchanged**

```bash
(cd yt-analyst && .venv/bin/python yta.py env --no-check)
(cd discord-reader && .venv/bin/python dread.py env --no-check)
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: both print `vault file : /home/vault/DReader/env` and a `credential : GEMINI_API_KEY, N chars, sha256:…` line with the same digest. The oracle prints four `identical`.

- [ ] **Step 9: Commit**

```bash
git add dreader_core tests yt-analyst/yta.py discord-reader/dread.py
git commit -m "[dr-dqm.1] dreader_core.creds: one credential loader for both collectors"
```

---

### Task 3: `dreader_core.gemini` — one retry, one parser

**Files:**
- Create: `dreader_core/gemini.py`, `tests/dreader_core/test_gemini.py`
- Modify: `tests/test_tools_delegate.py` (extend `PRIVATE_COPIES`)
- Modify: `yt-analyst/yta.py`, `discord-reader/dread.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/dreader_core/test_gemini.py`:
```python
import httpx
import pytest
from google.genai import errors, types

from dreader_core import gemini


def api_error(code):
    return errors.APIError(code, {"error": {"message": f"http {code}", "status": "X"}})


class FakeModels:
    def __init__(self, script):
        self.script = {m: list(v) for m, v in script.items()}
        self.calls = []

    def generate_content(self, model, contents, config):
        self.calls.append(model)
        outcome = self.script[model].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FakeClient:
    def __init__(self, script):
        self.models = FakeModels(script)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(gemini.time, "sleep", lambda s: None)


def test_retries_a_503_then_answers():
    c = FakeClient({"m": [api_error(503), "ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("m", "ok")
    assert c.models.calls == ["m", "m"]


def test_falls_back_after_exhausting_the_primary(monkeypatch):
    monkeypatch.setattr(gemini, "FALLBACK_MODELS", ["fb"])
    c = FakeClient({"m": [api_error(503)] * gemini.MAX_ATTEMPTS, "fb": ["ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("fb", "ok")


def test_non_retryable_on_the_primary_is_the_answer():
    c = FakeClient({"m": [api_error(400)]})
    with pytest.raises(errors.APIError) as e:
        gemini.generate_with_retry(c, "m", None, None)
    assert e.value.code == 400


def test_a_dead_fallback_is_skipped_and_the_original_error_kept(monkeypatch):
    monkeypatch.setattr(gemini, "FALLBACK_MODELS", ["retired"])
    c = FakeClient({"m": [api_error(503)] * gemini.MAX_ATTEMPTS,
                    "retired": [api_error(404)]})
    with pytest.raises(errors.APIError) as e:
        gemini.generate_with_retry(c, "m", None, None)
    assert e.value.code == 503


def test_transport_error_is_retried_like_a_503():
    c = FakeClient({"m": [httpx.RemoteProtocolError("Server disconnected"), "ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("m", "ok")


def test_no_retired_model_in_the_fallback_chain():
    # gemini-2.5-flash was retired 2026-09-06 [dr-9qo]; dread.py kept it until dr-dqm.
    assert "gemini-2.5-flash" not in gemini.FALLBACK_MODELS


def test_parse_plain_and_fenced_json():
    assert gemini.parse_json_reply('{"a": 1}') == {"a": 1}
    assert gemini.parse_json_reply('```json\n{"a": 1}\n```') == {"a": 1}


def test_parse_garbage_keeps_the_callers_shape():
    out = gemini.parse_json_reply("not json", shape={"summary": None, "claims": []})
    assert list(out) == ["summary", "claims", "uncertainties", "raw_unparsed", "empty_response"]
    assert out["raw_unparsed"] == "not json"


class Resp:
    text = None
    candidates = [type("C", (), {"finish_reason": "SAFETY"})()]
    prompt_feedback = None


def test_empty_reply_is_diagnosed_not_crashed():
    text, diag = gemini.response_text(Resp(), "m")
    assert text == "" and diag["finish_reasons"] == ["SAFETY"]


@pytest.mark.parametrize("res,expected", [
    (None, None), ("default", None),
    ("low", types.MediaResolution.MEDIA_RESOLUTION_LOW),
    ("high", types.MediaResolution.MEDIA_RESOLUTION_HIGH),
])
def test_media_config(res, expected):
    assert gemini.media_config(res).media_resolution == expected
```
Also create an empty `tests/dreader_core/__init__.py` if pytest complains about duplicate basenames (it will not with rootdir-relative ids, so try without first).

- [ ] **Step 2: Run and watch it fail**

Run: `.venv/bin/pytest tests/dreader_core/test_gemini.py -q`
Expected: `ImportError: cannot import name 'gemini' from 'dreader_core'`.

- [ ] **Step 3: Implement**

Create `dreader_core/gemini.py`:
```python
"""Calling Gemini: which model, how to survive a busy one, how to read what it
says. yta.py's versions, which were the more hardened, are the ones kept;
dread.py inherits their fixes [dr-dqm.1]."""
import json
import logging
import re
import sys
import time
import warnings

DEFAULT_MODEL = "gemini-flash-latest"
# gemini-2.5-flash was retired 2026-09-06 and now 404s for new users,
# which turned a transient 503 into a hard traceback [dr-9qo].
FALLBACK_MODELS = ["gemini-3.6-flash"]
RETRYABLE = {429, 500, 503}
MAX_ATTEMPTS = 4
BASE_DELAY_S = 5


def quiet_sdk():
    warnings.filterwarnings("ignore")
    for name in ("google_genai", "google.genai", "google_genai.models"):
        logging.getLogger(name).setLevel(logging.ERROR)


def media_config(resolution, **kw):
    """GenerateContentConfig with the media_resolution knob applied. None and
    "default" leave the knob unset (yta passed None, dread passed "default")."""
    from google.genai import types
    if resolution and resolution != "default":
        kw["media_resolution"] = getattr(
            types.MediaResolution, f"MEDIA_RESOLUTION_{resolution.upper()}")
    return types.GenerateContentConfig(**kw)


def parse_json_reply(text, empty_diag=None, shape=None):
    """The reply as JSON; fences stripped if the model added them. When it is
    not JSON at all, return the caller's empty shape with the raw text kept."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            out = dict(shape or {})
            out.update({"uncertainties": [], "raw_unparsed": text,
                        "empty_response": empty_diag})
            return out
```
Then add `response_text` and `generate_with_retry`, copied **verbatim** from yta.py (lines 408–419 and 458–501). They refer to `FALLBACK_MODELS`, `MAX_ATTEMPTS`, `BASE_DELAY_S` and `RETRYABLE` as module globals, and `time.sleep` through the module's `time`, which is what the tests monkeypatch.

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/pytest tests/dreader_core/test_gemini.py -q`
Expected: all pass.

- [ ] **Step 5: Extend the delegation test**

In `tests/test_tools_delegate.py`, extend `PRIVATE_COPIES` with:
```python
                  "generate_with_retry", "parse_json_reply", "response_text",
                  "quiet_sdk", "FALLBACK_MODELS", "RETRYABLE",
```
Run: `.venv/bin/pytest tests/test_tools_delegate.py -q`. Expected: FAIL, naming `generate_with_retry` on both tools.

- [ ] **Step 6: Wire yta.py**

Change the import to `from dreader_core import creds, gemini  # noqa: E402`. Delete `DEFAULT_MODEL`, `FALLBACK_MODELS`, `RETRYABLE`, `MAX_ATTEMPTS`, `BASE_DELAY_S`, `quiet_sdk`, `resolution_config`, `parse_json_reply`, `response_text` and `generate_with_retry`. Then add, next to `ANALYST_PROMPT`:
```python
# The empty-reply shape an ask or transcribe falls back to when Gemini's reply
# is not JSON — the keys the curated tooling reads first.
ASK_SHAPE = {"summary": None, "claims": []}
```
Replace every call:
- `generate_with_retry(` → `gemini.generate_with_retry(`
- `response_text(` → `gemini.response_text(`
- `parse_json_reply(text, empty_diag)` → `gemini.parse_json_reply(text, empty_diag, ASK_SHAPE)`
- `resolution_config(` → `gemini.media_config(`
- `quiet_sdk()` → `gemini.quiet_sdk()`
- `default=DEFAULT_MODEL` → `default=gemini.DEFAULT_MODEL`

Remove any import this leaves unused: check `warnings` and `logging` with `/usr/bin/grep -nw 'warnings\|logging' yt-analyst/yta.py`.

- [ ] **Step 7: Wire dread.py, taking the fixes it lacked**

Change the import to `from dreader_core import creds, gemini  # noqa: E402`. Delete `DEFAULT_MODEL`, `FALLBACK_MODELS`, `RETRYABLE`, `MAX_ATTEMPTS`, `BASE_DELAY_S`, `quiet_sdk`, `gen_config`, `generate_with_retry` and `parse_json_reply`. Add:
```python
TRANSCRIPT_SHAPE = {"context": None, "messages": []}
```
In `transcribe()`: `gen_config(` → `gemini.media_config(`, and `generate_with_retry(` → `gemini.generate_with_retry(`.
In `cmd_ingest`, replace `payload = parse_json_reply(resp.text)` with:
```python
    text, empty_diag = gemini.response_text(resp, answered_model)
    payload = gemini.parse_json_reply(text, empty_diag, TRANSCRIPT_SHAPE)
```
In `cmd_ask`: `gen_config(` → `gemini.media_config(`, `generate_with_retry(` → `gemini.generate_with_retry(`. Replace both `resp.text` uses with `text` from:
```python
    text, _ = gemini.response_text(resp, answered_model)
```
In `main()`: `quiet_sdk()` → `gemini.quiet_sdk()`, and `default=DEFAULT_MODEL` → `default=gemini.DEFAULT_MODEL` (twice).

- [ ] **Step 8: Verify**

```bash
.venv/bin/pytest tests -q
(cd discord-reader && .venv/bin/python dread.py --help >/dev/null && echo dread-ok)
(cd yt-analyst && .venv/bin/python yta.py --help >/dev/null && echo yta-ok)
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: all pass, `dread-ok`, `yta-ok`, four `identical`.

- [ ] **Step 9: Commit**

```bash
git add dreader_core tests yt-analyst/yta.py discord-reader/dread.py
git commit -m "[dr-dqm.1] dreader_core.gemini: one retry/fallback path; dread.py drops the retired gemini-2.5-flash fallback and gains transport-error retry and the empty-reply guard"
```

---

### Task 4: `dreader_core.uploads` and `dreader_core.runs`

**Files:**
- Create: `dreader_core/uploads.py`, `dreader_core/runs.py`
- Create: `tests/dreader_core/test_uploads.py`, `tests/dreader_core/test_runs.py`
- Modify: `tests/test_tools_delegate.py`, `yt-analyst/yta.py`, `discord-reader/dread.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/dreader_core/test_runs.py`:
```python
from datetime import datetime

from dreader_core import runs


class FrozenDT(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 25, 12, 0, 0)


def test_two_runs_in_one_second_get_two_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(runs, "datetime", FrozenDT)
    ts1, d1 = runs.new_run_dir(tmp_path)
    ts2, d2 = runs.new_run_dir(tmp_path)
    assert (ts1, ts2) == ("20260925-120000", "20260925-120000-2")
    assert d1.is_dir() and d2.is_dir() and d1 != d2
    assert d1.parent == tmp_path / "runs"


def test_run_log_appends_one_line(tmp_path):
    card = tmp_path / "CARD.md"
    card.write_text("# x\n")
    runs.append_run_log(card, "- a   \n")
    assert card.read_text() == "# x\n- a\n"


def test_timestamps_round_trip():
    assert runs.parse_ts("1:02:03") == 3723
    assert runs.parse_ts("05:30") == 330
    assert runs.parse_ts("95") == 95
    assert runs.parse_ts(None) is None
    assert runs.fmt_ts(3723) == "1:02:03"
    assert runs.fmt_ts(330) == "5:30"
```

Create `tests/dreader_core/test_uploads.py`:
```python
import types as pytypes

from dreader_core import uploads


def fobj(name, state="ACTIVE"):
    return pytypes.SimpleNamespace(name=name, uri=f"uri/{name}", mime_type="video/mp4",
                                   state=pytypes.SimpleNamespace(name=state))


class FakeFiles:
    def __init__(self, states=("ACTIVE",)):
        self.uploads, self.configs, self._states = 0, [], list(states)

    def upload(self, file, config=None):
        self.uploads += 1
        self.configs.append(config)
        return fobj(f"files/{self.uploads}", self._states[0])

    def get(self, name):
        state = self._states.pop(0) if len(self._states) > 1 else self._states[0]
        return fobj(name, state)


class FakeClient:
    def __init__(self, **kw):
        self.files = FakeFiles(**kw)


def test_second_call_reuses_the_cached_handle(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 1


def test_a_changed_file_is_uploaded_again(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    src.write_bytes(b"x" * 11)
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 2


def test_waits_out_processing(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x")
    c = FakeClient(states=("PROCESSING", "PROCESSING", "ACTIVE"))
    assert uploads.upload_file(c, src).state.name == "ACTIVE"


def test_mime_type_is_passed_when_given(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.pdf"
    src.write_bytes(b"%PDF")
    c = FakeClient()
    uploads.upload_file(c, src, mime_type="application/pdf")
    assert c.files.configs == [{"mime_type": "application/pdf"}]
```

- [ ] **Step 2: Run and watch them fail**

Run: `.venv/bin/pytest tests/dreader_core -q`
Expected: `ImportError: cannot import name 'runs'` and `… 'uploads'`.

- [ ] **Step 3: Implement `runs.py`**

```python
"""Run archives: every Gemini call leaves runs/<timestamp>/ and one line in the
dossier card's run log."""
from datetime import datetime


def new_run_dir(dossier):
    """(ts, path) of a fresh dossier/runs/<ts>/. Parallel asks can share a
    second [dr-8qq.11]; never overwrite an archive."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = dossier / "runs" / ts
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        try:
            run_dir.mkdir()
            return ts, run_dir
        except FileExistsError:
            n += 1
            ts = f"{ts.split('-')[0]}-{ts.split('-')[1]}-{n}"
            run_dir = run_dir.parent / ts


def append_run_log(card, line):
    with open(card, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def parse_ts(s):
    """'HH:MM:SS' | 'MM:SS' | '95' -> seconds."""
    if s is None:
        return None
    sec = 0
    for p in str(s).split(":"):
        sec = sec * 60 + int(p)
    return sec


def fmt_ts(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"
```

- [ ] **Step 4: Implement `uploads.py`**

```python
"""Gemini Files API: upload once, reuse the handle for 48 h."""
import json
import sys
import time
from datetime import datetime

UPLOAD_TTL_S = 47 * 3600  # Files API keeps an upload 48 h; leave a margin


def upload_file(client, path, mime_type=None):
    """Upload and wait until ACTIVE. No cache — dread.py deletes its upload
    after one use; media-reader goes through upload_cached."""
    print(f"[uploading {path.name} ({path.stat().st_size / 1e6:.0f} MB)...]",
          file=sys.stderr)
    t0 = time.time()
    f = client.files.upload(file=str(path),
                            config={"mime_type": mime_type} if mime_type else None)
    while f.state.name == "PROCESSING":
        time.sleep(4)
        f = client.files.get(name=f.name)
    if f.state.name != "ACTIVE":
        sys.exit(f"Upload failed: file state {f.state.name}")
    print(f"[upload active: {f.name} in {time.time() - t0:.0f}s]", file=sys.stderr)
    return f


def upload_cached(client, cache, path, mime_type=None):
    """Upload through the Files API once; reuse the handle recorded in `cache`
    (a JSON file) while it is fresh, the same file, and ACTIVE server-side.
    Uploads of ~1 GB take minutes over the WSL bridge; the cache is what makes
    clipped follow-ups near-free."""
    if cache.exists():
        try:
            rec = json.loads(cache.read_text())
            if (rec.get("path") == str(path) and rec.get("size") == path.stat().st_size
                    and rec.get("expires", 0) > time.time() + 300):
                f = client.files.get(name=rec["name"])
                if f.state.name == "ACTIVE":
                    print(f"[upload reused: {f.name}, expires "
                          f"{datetime.fromtimestamp(rec['expires']):%Y-%m-%d %H:%M}]",
                          file=sys.stderr)
                    return f
        except Exception as e:  # stale, expired, deleted server-side
            print(f"[upload cache unusable: {e}; re-uploading]", file=sys.stderr)
    f = upload_file(client, path, mime_type)
    cache.write_text(json.dumps({
        "name": f.name, "uri": f.uri, "mime_type": f.mime_type,
        "path": str(path), "size": path.stat().st_size,
        "uploaded": datetime.now().isoformat(timespec="seconds"),
        "expires": time.time() + UPLOAD_TTL_S,
    }, indent=2))
    return f
```

- [ ] **Step 5: Run the core tests**

Run: `.venv/bin/pytest tests/dreader_core -q`
Expected: all pass.

- [ ] **Step 6: Wire both tools and extend the delegation test**

Add to `PRIVATE_COPIES`: `"new_run_dir", "append_run_log", "upload_video", "upload_cached", "UPLOAD_TTL_S"`.

yta.py: import becomes `from dreader_core import creds, gemini, runs, uploads  # noqa: E402`. Delete `UPLOAD_TTL_S`, `upload_cached`, `new_run_dir`, `append_run_log`, `parse_ts` and `fmt_ts`. Then:
- in `video_part_for`: `g = upload_cached(client, vid, path)` → `g = uploads.upload_cached(client, video_dir(vid) / "upload.json", path)`
- `new_run_dir(vid)` → `runs.new_run_dir(video_dir(vid))`
- `append_run_log(` → `runs.append_run_log(`
- keep `parse_ts`/`fmt_ts` callable under their short names, because index/export/transcribe use them in many places. Add, under the import:
```python
parse_ts, fmt_ts = runs.parse_ts, runs.fmt_ts
```

dread.py: import becomes `from dreader_core import creds, gemini, runs, uploads  # noqa: E402`. Delete `upload_video` and `append_run_log`. Then:
- `upload_video(client, …)` → `uploads.upload_file(client, …)` (both call sites; the delete-after-use lines stay)
- `append_run_log(` → `runs.append_run_log(`
- in `cmd_ask`, replace
  ```python
      ts = datetime.now().strftime("%Y%m%d-%H%M%S")
      run_dir = dossier / "runs" / ts
      run_dir.mkdir(parents=True, exist_ok=True)
  ```
  with `ts, run_dir = runs.new_run_dir(dossier)`

- [ ] **Step 7: Verify, including one live call per tool**

```bash
.venv/bin/pytest tests -q
.venv/bin/python tests/media_reader/compare_outputs.py check
(cd yt-analyst && .venv/bin/python yta.py ask --url "https://www.youtube.com/watch?v=IUWvHVout94" \
   --start 0:30 --end 1:00 --question "What is on screen? (dr-dqm.1 smoke test)" | head -5)
ls discord-reader/captures/
(cd discord-reader && .venv/bin/python dread.py ask --capture 20260912-103808-investitrade-lessons-key-zones \
   --question "How many messages are visible? (dr-dqm.1 smoke test)" | head -5)
```
The capture id is the `…-key-zones` directory under `discord-reader/captures/`; take the exact name from the `ls`. Expected: tests pass, four `identical`, and two answers, each archived under a fresh `runs/<ts>/` with one new run-log line on its card. The yta ask adds a run-log line to `IUWvHVout94/CARD.md`, which changes that card's `Runs` count. Rerun `compare_outputs.py save` right after this step, so the next task's check starts from the new count.

- [ ] **Step 8: Commit**

```bash
git add dreader_core tests yt-analyst/yta.py discord-reader/dread.py yt-analyst/videos/IUWvHVout94/CARD.md
git commit -m "[dr-dqm.1] dreader_core.uploads + runs; dread.py run dirs no longer collide within a second"
```

---

### Task 5: Rename `yt-analyst/` → `media-reader/`, `yta.py` → `mread.py`

**Files:** the directory itself. References are listed in step 6. `docs/retired/REGISTER.md`, `.gitleaks.toml`.

- [ ] **Step 1: Preconditions**

```bash
pgrep -af 'yta.py|build_reader|build_corpus' || echo "nothing running"
git status --short yt-analyst
```
Expected: `nothing running`, and no output from `git status`. Commit or stash anything it shows before continuing.

- [ ] **Step 2: Move the directory with its untracked working data**

```bash
mv yt-analyst media-reader
git add -A yt-analyst media-reader
git mv media-reader/yta.py media-reader/mread.py
git status --short | /usr/bin/grep -v '^R ' | head
```
Plain `mv` carries the gitignored data along: `runs/`, `frames-*`, `upload.json`, transcripts, `.venv`. Expected: no line other than renames (`R `) from the last command.

- [ ] **Step 3: Rebuild the venv (its scripts hard-code the old path)**

```bash
rm -rf media-reader/.venv
python3 -m venv media-reader/.venv
media-reader/.venv/bin/pip install -q -r media-reader/requirements.txt
media-reader/.venv/bin/python -c "import google.genai, httpx; print('venv ok')"
head -1 media-reader/.venv/bin/yt-dlp
```
Expected: `venv ok`, and a shebang naming `/root/projects/DReader/media-reader/.venv/bin/python`.

- [ ] **Step 4: Rename the tool's self-references**

In `media-reader/mread.py`, change these (all are user-facing strings):
- module docstring line 2: `"""yta.py v0.4 — YouTube analyst: Gemini Flash as a perception service.` → `"""mread.py v0.5 — media-reader: Gemini Flash as a perception service over media.`, and add a `Changes from v0.4:` paragraph: *renamed from yt-analyst/yta.py (dr-dqm); credentials, retry, uploads and run archives now come from dreader_core, shared with discord-reader.*
- every remaining `yta.py` inside a string → `mread.py` (`/usr/bin/grep -n 'yta\.py' media-reader/mread.py` lists them: the card templates' run-log line, `creds.require_key(…)`, `creds.report_env(…)`, the slides.md banner, the index banner, the export `generator`)
- the browser's `yt-analyst — video cards` / `<h1>yt-analyst</h1>` / `" — yt-analyst"` → `media-reader`

- [ ] **Step 5: Leave a forwarding shim at the old name**

Create `media-reader/yta.py`:
```python
#!/usr/bin/env python3
"""yta.py was renamed mread.py on 2026-09-25 [dr-dqm]. This forwards, and says
so, so an old note or a sibling's copied command still works."""
import os
import sys
from pathlib import Path

target = Path(__file__).resolve().with_name("mread.py")
print("[yta.py is now mread.py — forwarding; update the command]", file=sys.stderr)
os.execv(sys.executable, [sys.executable, str(target), *sys.argv[1:]])
```

- [ ] **Step 6: Update the references that are live instructions or code**

Update these files. `/usr/bin/grep -n 'yt-analyst\|yta\.py' <file>` finds the lines; replace `yt-analyst/` → `media-reader/` and `yta.py` → `mread.py`:
- `CLAUDE.md` (root): Architecture, Key Files table, Key Commands. Describe `media-reader/` as *media ingestion — YouTube, local captures, and (Plan B) audio, images, documents — as dossiers*.
- `media-reader/CLAUDE.md`: title becomes `# media-reader — operating instructions for Claude Code`, and every command
- `media-reader/UI-BRIEF.md`, `media-reader/build_corpus.py` (docstring), `media-reader/newsletters/tradebrigade/README.md`
- `.claude/skills/composing-card-reads/SKILL.md`, `.claude/skills/narrating-orderflow/SKILL.md`
- `.gitleaks.toml`: `'''^yt-analyst/videos/[^/]+/runs/'''` → `'''^media-reader/videos/[^/]+/runs/'''` and `'''^yt-analyst/browser\.html$'''` → `'''^media-reader/browser\.html$'''`
- `tests/test_tools_delegate.py`: leave both candidate paths; the fixture takes whichever exists

Leave these alone; they are dated history: `LESSONS.md`, `AUDIT.md`, `EDITS.md`, `docs/2026-09-18-*.md`, `.beads/`, every `CARD.md`/`READ.md`. Add one line under the title of `media-reader/LESSONS.md`:
```markdown
_Entries before 2026-09-25 say `yt-analyst/` and `yta.py`: the directory and the tool were renamed `media-reader/` and `mread.py` that day (dr-dqm). Commands still work through the `yta.py` shim._
```

- [ ] **Step 7: Keep the newsletter ingester finding its transcripts**

Claude Code names a session's transcript directory after its working directory, so sessions started in `media-reader/` write under a new path. In `media-reader/newsletters/tradebrigade/ingest.py`, replace line 18:
```python
DEFAULT_SRC = (glob.glob("/root/.claude/projects/-root-projects-DReader-yt-analyst/*/tool-results")
               + glob.glob("/root/.claude/projects/-root-projects-DReader-media-reader/*/tool-results"))
```

- [ ] **Step 8: Completeness sweep**

```bash
/usr/bin/grep -rnI 'yt-analyst\|yta\.py' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.beads \
  --exclude-dir=videos --exclude-dir=node_modules . \
  | /usr/bin/grep -v 'LESSONS.md\|AUDIT.md\|EDITS.md\|docs/2026-09-18\|\.refactor-\|compare_outputs.py\|test_tools_delegate.py\|media-reader/yta.py\|ingest.py:1[89]'
```
Expected: only generated files (`browser.html`, `reader.html`, `corpus.json`, `design/reading-ui/*.html`). Anything else is a missed live reference, so fix it.

- [ ] **Step 9: Record the retirement**

Add under `## Retirements` in `docs/retired/REGISTER.md`, above the 09-18 entry:
```markdown
### 2026-09-25 — the name yt-analyst  [dr-dqm]

Steve's ruling (2026-09-18, confirmed 09-25): *"the name YouTube-Analyst is too
YouTube specific … this repository manages media ingestion."* Renamed
`yt-analyst/` → `media-reader/`, `yta.py` → `mread.py`. `media-reader/yta.py` is a
forwarding shim that says so on stderr.

**Invalidates:**

- the path `yt-analyst/` in any command, doc or config (history files keep it)
- `yta.py` as the tool's name (the shim forwards; do not add features to it)
- `/root/.claude/projects/-root-projects-DReader-yt-analyst/` as where new
  session transcripts land (the newsletter ingester reads both)
- the premise that each collector keeps its own copy of credential, retry and
  upload code "by design" — `dreader_core/` holds the one copy, and
  `tests/test_tools_delegate.py` fails if a copy grows back

**Do not propose:** folding discord-reader into media-reader. Steve ruled 09-25
that it shares the core only.
```

- [ ] **Step 10: Verify**

```bash
.venv/bin/pytest tests -q
(cd media-reader && .venv/bin/python mread.py env --no-check | head -1)
(cd media-reader && .venv/bin/python yta.py index --stdout | head -1)
.venv/bin/python tests/media_reader/compare_outputs.py check
```
Expected: pass. Then `vault file : /home/vault/DReader/env`, then the forwarding notice on stderr and `# Video index`, then four `identical` (the renames are normalised).

- [ ] **Step 11: Commit, then tell the siblings**

```bash
git add -A media-reader yt-analyst CLAUDE.md .claude/skills .gitleaks.toml docs/retired/REGISTER.md tests
git commit -m "[dr-dqm.1] Rename yt-analyst → media-reader, yta.py → mread.py (Steve 2026-09-18/25); yta.py forwards"
```
DReader writes only to its own repo, so Strader (3 documents) and COO (`factory/scripts/vault-status.py` prints `DReader (yta.py, dread.py)`) get mail, not edits. Run `gc mail --help` and the gc-agents skill's list command to find the two addresses. Then send each:
```
gc mail send <address> -s "DReader: yt-analyst renamed media-reader [dr-dqm]" -m "yt-analyst/ is now media-reader/ and yta.py is mread.py (Steve's ruling). yta.py still works and forwards with a notice. Your references: <Strader: docs/plans/youtube-ingestion-plan.md, docs/plans/2026-09-18-icm-applied-to-narrating-orderflow.md, docs/a2a/inbox.md | COO: factory/scripts/vault-status.py line 143 label>. Update at your convenience; nothing breaks meanwhile. Register entry: DReader docs/retired/REGISTER.md."
```

---

### Task 6: `videos/` → `dossiers/`

A PDF or a podcast in a directory called `videos/` repeats the naming problem this plan exists to fix, so the dossier directory is renamed before Plan B adds non-video kinds.

**Files:** `media-reader/{mread.py,build_corpus.py,build_reader.py,fetch_transcripts.py,fetch_thumbs.py,.gitignore,CLAUDE.md,UI-BRIEF.md}`, `media-reader/playlists/*.md`, both skills, `.gitleaks.toml`, `docs/retired/REGISTER.md`

- [ ] **Step 1: Move**

```bash
mv media-reader/videos media-reader/dossiers
git add -A media-reader/videos media-reader/dossiers
```

- [ ] **Step 2: Code**

- `mread.py`: `VIDEOS_DIR = SCRIPT_DIR / "videos"` → `DOSSIERS_DIR = SCRIPT_DIR / "dossiers"`. Rename every use of `VIDEOS_DIR` to `DOSSIERS_DIR`, and every string literal `videos/` to `dossiers/` (`/usr/bin/grep -n 'VIDEOS_DIR\|videos/' media-reader/mread.py`). Set `EXPORT_SCHEMA_VERSION = 2`, and add to the export's `contract` block, as its **first** key (so no neighbouring line gains or loses a comma, and the oracle's normalisation rule for it removes exactly one line), `"changes_from_v1": "card paths moved from videos/<id>/ to dossiers/<id>/ (dr-dqm, 2026-09-25); ids unchanged"`.
- `build_corpus.py`, `fetch_transcripts.py`: `VIDEOS = ROOT / "videos"` → `VIDEOS = ROOT / "dossiers"`
- `build_reader.py` line 34 and `fetch_thumbs.py` line 15: `ROOT / "videos"` → `ROOT / "dossiers"`
- `media-reader/.gitignore`: every `videos/*/` → `dossiers/*/`
- `.gitleaks.toml`: `^media-reader/videos/` → `^media-reader/dossiers/`

- [ ] **Step 3: The 31 relative links in playlist syntheses**

```bash
sed -i 's#](\.\./videos/#](../dossiers/#g' media-reader/playlists/*.md
/usr/bin/grep -c '\.\./videos/' media-reader/playlists/*.md
```
Expected: every count is `0`. The 654 `../<id>/CARD.md` links between cards are relative within the directory and need no change.

- [ ] **Step 4: Docs**

`media-reader/CLAUDE.md`, `UI-BRIEF.md` and both skills: `videos/<id>` → `dossiers/<id>`, `videos/*/` → `dossiers/*/`. The *Dossier layout* section opens: *Every piece of media gets a directory: `dossiers/<id>/`.* Append to the 09-25 register entry's **Invalidates:** list: `- videos/<id>/ as a dossier path; export schema_version 1 (paths) — now 2`.

- [ ] **Step 5: Sweep and verify**

```bash
/usr/bin/grep -rnI '\bvideos/' media-reader --include=*.py --include=*.md --include=.gitignore \
  | /usr/bin/grep -v 'LESSONS.md\|AUDIT.md\|EDITS.md\|/dossiers/.*/\(CARD\|READ\).md'
.venv/bin/pytest tests -q
.venv/bin/python tests/media_reader/compare_outputs.py check
(cd media-reader && python3 build_corpus.py && python3 build_reader.py)
```
Expected: the sweep prints nothing, tests pass, four `identical`. `reader.html` rebuilds. Republish it to the reader Artifact URL recorded on bead dr-gm5, using the Artifact tool's publish with that `url`.

- [ ] **Step 6: Commit**

```bash
git add -A media-reader .claude/skills .gitleaks.toml docs/retired/REGISTER.md
git commit -m "[dr-dqm.1] videos/ → dossiers/: the dossier directory stops naming one media kind; export schema v2"
```

---

### Task 7: Split `mread.py` by responsibility

Mechanical: functions move **verbatim** into modules, and no body changes. The oracle is the test.

**Files:** create `media-reader/{sources,prompts,perceive,verify,corpus}.py`, shrink `media-reader/mread.py`

- [ ] **Step 1: Create the modules and move code into them**

Each module starts with the same three lines, then the imports its moved code needs:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # dreader_core
```

| Module | Moves in (by name) | Imports it needs |
|---|---|---|
| `prompts.py` | `ANALYST_PROMPT`, `TRANSCRIBE_PROMPT`, `ASK_SHAPE` | — |
| `sources.py` | `SCRIPT_DIR`, `DOSSIERS_DIR`, `CARD_TEMPLATE`, `CARD_TEMPLATE_LOCAL`, `LOCAL_ID_RE`, `extract_video_id`, `canonical_url`, `video_dir`, `ensure_card`, `probe_duration`, `resolve_source`, `video_part_for` | `re, subprocess, sys, datetime, Path`; `from dreader_core import uploads`; `from dreader_core.runs import fmt_ts` |
| `perceive.py` | `cmd_ask`, `chunk_offset`, `cmd_transcribe` | `json, subprocess, sys, datetime`; `from dreader_core import creds, gemini, runs`; `from dreader_core.runs import parse_ts, fmt_ts`; `from prompts import *`; `from sources import resolve_source, video_dir, video_part_for, probe_duration` |
| `verify.py` | `cmd_frames` | `subprocess, sys, Path`; `from dreader_core.runs import parse_ts, fmt_ts`; `from sources import resolve_source, video_dir` |
| `corpus.py` | everything from the `# ---- index ----` banner to the end of `cmd_browse`: `INDEX_PATH` … `render_browser`, `cmd_browse`, `BROWSER_TEMPLATE` | `json, re, sys, datetime, Path`; `from dreader_core.runs import fmt_ts`; `from sources import SCRIPT_DIR, DOSSIERS_DIR` |

In `perceive.py`, `creds.require_key("mread.py")` stays as it is.

- [ ] **Step 2: Leave `mread.py` as the CLI**

`mread.py` keeps its module docstring (it is the `--help` text), the `sys.path` insert, and:
```python
from dreader_core import creds, gemini  # noqa: E402
from corpus import cmd_index, cmd_export, cmd_browse, BROWSER_PATH  # noqa: E402
from perceive import cmd_ask, cmd_transcribe  # noqa: E402
from sources import SCRIPT_DIR  # noqa: E402
from verify import cmd_frames  # noqa: E402


def cmd_env(args):
    creds.report_env(SCRIPT_DIR, "mread.py", args.no_check)
```
and `main()` unchanged.

- [ ] **Step 3: Nothing left behind, nothing duplicated**

```bash
cd media-reader
wc -l mread.py sources.py prompts.py perceive.py verify.py corpus.py
for f in sources prompts perceive verify corpus; do .venv/bin/python -c "import $f" || echo "BROKEN $f"; done
.venv/bin/python -m pyflakes *.py 2>/dev/null || .venv/bin/pip install -q pyflakes && .venv/bin/python -m pyflakes mread.py sources.py prompts.py perceive.py verify.py corpus.py
cd ..
```
Expected: `mread.py` under 120 lines, the parts summing to roughly the old total, no `BROKEN`, and no pyflakes `undefined name` (an unused import is a warning to clean up, not a failure).

- [ ] **Step 4: Verify**

```bash
.venv/bin/pytest tests -q
.venv/bin/python tests/media_reader/compare_outputs.py check
for c in ask frames transcribe index browse export env; do (cd media-reader && .venv/bin/python mread.py $c --help >/dev/null) || echo "BROKEN $c"; done
```
Expected: pass, four `identical`, no `BROKEN`.

- [ ] **Step 5: Commit**

```bash
git add media-reader
git commit -m "[dr-dqm.1] Split mread.py into sources/prompts/perceive/verify/corpus; bodies unchanged"
```

---

### Task 8: The source seam — `Source` and kinds

**Files:** modify `media-reader/sources.py`, `perceive.py`, `verify.py`, `corpus.py`; create `tests/media_reader/test_sources.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/media_reader/test_sources.py`:
```python
import argparse

import pytest

import sources


@pytest.fixture(autouse=True)
def tmp_dossiers(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")


def ns(**kw):
    base = {"url": None, "file": None, "id": None}
    base.update(kw)
    return argparse.Namespace(**base)


def test_youtube_url_resolves_to_a_youtube_source():
    s = sources.resolve_source(ns(url="https://youtu.be/IUWvHVout94?t=3"))
    assert (s.kind, s.id, s.url, s.path) == (
        "youtube", "IUWvHVout94", "https://www.youtube.com/watch?v=IUWvHVout94", None)
    assert s.card.exists() and "**Kind:** youtube" in s.card.read_text()


def test_mp4_file_resolves_to_a_video_source(tmp_path):
    f = tmp_path / "rec.mp4"
    f.write_bytes(b"\0")
    s = sources.resolve_source(ns(file=str(f), id="it-orderflow-test"))
    assert (s.kind, s.id, s.path) == ("video", "it-orderflow-test", f.resolve())
    assert "**Kind:** video" in s.card.read_text()


def test_file_needs_an_id(tmp_path):
    f = tmp_path / "rec.mp4"
    f.write_bytes(b"\0")
    with pytest.raises(SystemExit, match="needs --id"):
        sources.resolve_source(ns(file=str(f)))


def test_unknown_extension_is_refused_naming_the_known_ones(tmp_path):
    f = tmp_path / "notes.xyz"
    f.write_bytes(b"\0")
    with pytest.raises(SystemExit, match=r"unsupported.*\.mp4"):
        sources.resolve_source(ns(file=str(f), id="some-notes"))


def test_existing_cards_are_never_rewritten(tmp_path):
    d = sources.DOSSIERS_DIR / "IUWvHVout94"
    d.mkdir(parents=True)
    (d / "CARD.md").write_text("# Video: IUWvHVout94\ncurated\n")
    s = sources.resolve_source(ns(url="https://www.youtube.com/watch?v=IUWvHVout94"))
    assert s.card.read_text() == "# Video: IUWvHVout94\ncurated\n"
```

- [ ] **Step 2: Run and watch them fail**

Run: `.venv/bin/pytest tests/media_reader/test_sources.py -q`
Expected: failures on `.kind` (`AttributeError: 'tuple' object has no attribute 'kind'`) and on the unsupported-extension test.

- [ ] **Step 3: Implement the seam in `sources.py`**

Add at the top of `sources.py`, after the imports:
```python
from dataclasses import dataclass


@dataclass
class Source:
    """One piece of media and its dossier. `kind` decides the prompt, how the
    bytes reach Gemini, and which verification commands apply. Plan B adds
    "audio", "image" and "document" kinds; nothing else in the tool names a
    kind directly [dr-dqm]."""
    kind: str               # "youtube" | "video"
    id: str
    card: Path
    url: str | None = None
    path: Path | None = None
    mime: str | None = None


# Local file kinds, by extension. Plan B extends this table; the error message
# for an unknown extension lists whatever it holds.
KIND_BY_EXT = {
    ".mp4": ("video", "video/mp4"),
    ".mkv": ("video", "video/x-matroska"),
    ".mov": ("video", "video/quicktime"),
    ".webm": ("video", "video/webm"),
}


def kind_for(path):
    try:
        return KIND_BY_EXT[path.suffix.lower()]
    except KeyError:
        sys.exit(f"--file: unsupported type {path.suffix or '(none)'}; "
                 f"known: {' '.join(sorted(KIND_BY_EXT))}")
```
Add `- **Kind:** youtube` as the second list item of `CARD_TEMPLATE`, and `- **Kind:** {kind}` as the second list item of `CARD_TEMPLATE_LOCAL`. Rewrite `resolve_source` to return a `Source`. The validations and messages are unchanged; `kind_for` runs before the id checks. (The existing "looks like a YouTube id" guard is dead code: `extract_video_id` only matches after `v=`, `youtu.be/`, `embed/` or `shorts/`, which a slug never contains. It moves unchanged and untested. Fixing it is a behaviour change outside this plan; file it as a bead if it matters.)
```python
def resolve_source(args):
    """The Source named by --url or --file/--id; creates its card on first contact."""
    path = getattr(args, "file", None)
    if path:
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            sys.exit(f"--file: not a file: {path}")
        kind, mime = kind_for(path)
        vid = getattr(args, "id", None)
        if not vid or not LOCAL_ID_RE.match(vid):
            sys.exit("--file needs --id: a slug like it-orderflow-absorption-4142 "
                     "(lowercase letters, digits, hyphens; it names dossiers/<id>/)")
        if extract_video_id(vid + "x") and len(vid) == 11:
            sys.exit(f"--id {vid} looks like a YouTube id; pick a slug")
        card = video_dir(vid) / "CARD.md"
        if not card.exists():
            secs = probe_duration(path)
            card.write_text(CARD_TEMPLATE_LOCAL.format(
                video_id=vid, kind=kind, path=path, size_mb=path.stat().st_size / 1e6,
                duration=f"{fmt_ts(secs)} ({secs} s)" if secs else "duration unknown",
                date=datetime.now().strftime("%Y-%m-%d")))
        return Source(kind=kind, id=vid, card=card, path=path, mime=mime)
    url = getattr(args, "url", None)
    if not url:
        sys.exit("give --url (YouTube) or --file PATH --id ID (local file)")
    vid = extract_video_id(url)
    if not vid:
        sys.exit(f"Could not extract a YouTube video id from: {url}")
    url = canonical_url(vid)
    return Source(kind="youtube", id=vid, card=ensure_card(vid, url), url=url)
```
Replace `video_part_for(client, vid, url, path, vm_kwargs)` with:
```python
def media_part(client, src, vm_kwargs):
    """The Part that carries src's bytes to Gemini."""
    from google.genai import types
    if src.kind == "youtube":
        fd = types.FileData(file_uri=src.url)
    else:
        g = uploads.upload_cached(client, video_dir(src.id) / "upload.json",
                                  src.path, src.mime)
        fd = types.FileData(file_uri=g.uri, mime_type=g.mime_type)
    return types.Part(
        file_data=fd,
        video_metadata=types.VideoMetadata(**vm_kwargs) if vm_kwargs else None,
    )
```
Rename `video_dir` → `dossier_dir` everywhere (`/usr/bin/grep -rn video_dir media-reader/*.py`). The old name stays as an alias for any external caller: `video_dir = dossier_dir`.

- [ ] **Step 4: Callers take a `Source`**

- `perceive.cmd_ask`: `vid, url, path, card = resolve_source(args)` → `src = resolve_source(args)`. Then `media_part(client, src, vm_kwargs)`; `vid`→`src.id`, `url`→`src.url`, `path`→`src.path`, `card`→`src.card`. `request.json` gains `"kind": src.kind` as its first key.
- `perceive.cmd_transcribe`: after resolving,
  ```python
      if src.kind != "video":
          sys.exit(f"transcribe: {src.kind} sources are not supported yet "
                   "(YouTube videos get captions from fetch_transcripts.py)")
  ```
  and `video_part_for(client, vid, None, path, vm)` → `media_part(client, src, vm)`.
- `verify.cmd_frames`:
  ```python
      src = resolve_source(args)
      if src.kind not in ("youtube", "video"):
          sys.exit(f"frames: a {src.kind} source has no frames")
  ```
  then `path`→`src.path`, `url`→`src.url`, `vid`→`src.id`.
- `corpus.collect_videos`: add to each carded dict
  ```python
              "kind": f.get("Kind") or ("youtube" if (f.get("URL") or "").startswith("http") else "video"),
  ```
  Nothing renders it yet (Plan B, Task B5), so the oracle stays quiet.

- [ ] **Step 5: Run the tests**

Run: `.venv/bin/pytest tests -q`
Expected: all pass.

- [ ] **Step 6: Oracle**

Run: `.venv/bin/python tests/media_reader/compare_outputs.py check`
Expected: four `identical`. Existing cards are never rewritten, so the new `Kind` line appears only on cards created from now on.

- [ ] **Step 7: One live call through the seam, per path**

```bash
cd media-reader
.venv/bin/python mread.py ask --url "https://www.youtube.com/watch?v=IUWvHVout94" --start 0:30 --end 1:00 \
  --question "What is on screen? (dr-dqm.1 seam smoke test)" | head -3
ls /mnt/c/Users/steve/OneDrive/Videos/Captures/*.mp4 | head -3
.venv/bin/python mread.py ask --file "<one of those paths>" --id dr-dqm-seam-smoke --start 0:00 --end 0:30 \
  --question "What is on screen? (dr-dqm.1 seam smoke test)" | head -3
cat dossiers/dr-dqm-seam-smoke/CARD.md | head -5
rm -rf dossiers/dr-dqm-seam-smoke
cd ..
```
Expected: two JSON answers, and a card showing `- **Kind:** video`. The smoke dossier is then removed. It uploads a whole capture, so pick the smallest file listed.

- [ ] **Step 7b: Put the smoke-test run-log line back out of the oracle's way**

The URL ask added a run-log line to `IUWvHVout94/CARD.md`. Commit it with this task and run `compare_outputs.py save`, so Plan B starts from a fresh baseline.

- [ ] **Step 8: Commit and close the plan**

```bash
git add media-reader tests
git commit -m "[dr-dqm.1] Source seam: kind-aware resolution, media_part, kind recorded on new cards"
bd close dr-dqm.1
git pull --rebase && bd dolt push && git push && git status
```
Expected: `Your branch is up to date with 'origin/master'`.

---

## Done when

- `.venv/bin/pytest tests -q` passes, including the delegation test, on both tools.
- `compare_outputs.py check` shows four `identical` against the Task 1 baseline (re-saved only after smoke-test run-log lines).
- `dread.py` no longer names `gemini-2.5-flash` anywhere: `/usr/bin/grep -n 2.5-flash discord-reader/dread.py` prints nothing.
- The retirement register records the rename and the videos/ → dossiers/ move, with invalidated premises.
- Strader and COO have mail naming their stale references.
