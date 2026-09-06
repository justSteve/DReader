"""Credential loading for yt-analyst and discord-reader — the 2026-09-05
regression [co-yuyh9].

The credential sweep moved secret values into /home/vault/<project>/env, and
every shell already running on this box kept a dead April GEMINI_API_KEY. Both
scripts loaded their env with ``os.environ.setdefault``, so the dead key won
and every Gemini call came back ``API key not valid``; in a fresh shell, which
carries neither name, the same bug shows its other face — ``GEMINI_API_KEY not
set``. These tests pin the direction that fixes both: a value from a file
overwrites a value from the environment.

``yta.py`` and ``dread.py`` are standalone scripts beside their own data and
their own venvs, so the loader is duplicated between them by design. Every test
here runs against both — a fix applied to one and forgotten in the other fails.

Run: .venv/bin/pytest tests/credential_loading -q
"""

import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = {
    "yta": REPO_ROOT / "yt-analyst" / "yta.py",
    "dread": REPO_ROOT / "discord-reader" / "dread.py",
}


@pytest.fixture(params=sorted(SCRIPTS), ids=sorted(SCRIPTS))
def tool(request):
    """Import a script by path — neither is an importable package."""
    path = SCRIPTS[request.param]
    if not path.exists():
        # discord-reader has never been committed to this repo (2026-09-06), so
        # a clone has yta.py and not dread.py. Skip rather than fail.
        pytest.skip(f"{path.relative_to(REPO_ROOT)} is not present in this checkout")
    name = f"{request.param}_under_test"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    yield mod
    del sys.modules[name]


@pytest.fixture(autouse=True)
def pristine_environ():
    """load_env writes straight into os.environ, so restore it around every
    test — monkeypatch only rolls back names it set itself."""
    before = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(before)


def write_env(path, text, mode=0o600):
    path.write_text(text)
    path.chmod(mode)
    return path


def no_tree(tool, tmp_path, monkeypatch):
    """Point the script at a directory that holds no .env."""
    monkeypatch.setattr(tool, "SCRIPT_DIR", tmp_path / "no-tree")


# ─── parse_env_file ──────────────────────────────────────────────────────────

def test_parse_handles_export_quotes_comments_and_junk(tool, tmp_path):
    p = write_env(tmp_path / "env", "\n".join([
        "# a comment",
        "",
        "PLAIN=one",
        "export EXPORTED=two",
        'QUOTED="three"',
        "SINGLE='four'",
        "  SPACED  =  five  ",
        "no_equals_sign_here",
        "EMPTY=",
        "URL=https://example.com/a?b=c",
    ]))
    assert tool.parse_env_file(p) == {
        "PLAIN": "one",
        "EXPORTED": "two",
        "QUOTED": "three",
        "SINGLE": "four",
        "SPACED": "five",
        "EMPTY": "",
        "URL": "https://example.com/a?b=c",
    }


def test_parse_later_line_wins(tool, tmp_path):
    p = write_env(tmp_path / "env", "K=first\nK=second\n")
    assert tool.parse_env_file(p)["K"] == "second"


# ─── secrets_path ────────────────────────────────────────────────────────────

def test_pointer_names_the_file(tool, tmp_path, monkeypatch):
    p = write_env(tmp_path / "env", "K=v\n")
    monkeypatch.setenv(tool.SECRETS_POINTER, str(p))
    assert tool.secrets_path() == (p, True)


def test_default_used_when_present_and_no_pointer(tool, tmp_path, monkeypatch):
    p = write_env(tmp_path / "env", "K=v\n")
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", p)
    assert tool.secrets_path() == (p, False)


def test_no_vault_at_all(tool, tmp_path, monkeypatch):
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    assert tool.secrets_path() == (None, False)


def test_both_tools_read_the_same_vault_file(tool):
    """One key, one file — the two scripts must not drift apart on where it is."""
    assert tool.DEFAULT_SECRETS_PATH == Path("/home/vault/DReader/env")
    assert tool.SECRETS_POINTER == "DREADER_SECRETS_FILE"


# ─── load_env: the regression ────────────────────────────────────────────────

def test_vault_beats_a_stale_exported_key(tool, tmp_path, monkeypatch):
    """The whole bug in one assertion."""
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setenv("GEMINI_API_KEY", "dead-april-key")
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    no_tree(tool, tmp_path, monkeypatch)

    tool.load_env()

    assert os.environ["GEMINI_API_KEY"] == "live-key"


def test_ambient_google_api_key_is_evicted(tool, tmp_path, monkeypatch):
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setenv("GOOGLE_API_KEY", "some-other-google-key")
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    no_tree(tool, tmp_path, monkeypatch)

    tool.load_env()

    assert "GOOGLE_API_KEY" not in os.environ


def test_secret_in_the_tree_is_refused_and_reported(tool, tmp_path, monkeypatch, capsys):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_env(tree / ".env", "GEMINI_API_KEY=key-in-the-tree\nSETTING=kept\n")
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n")
    monkeypatch.setattr(tool, "SCRIPT_DIR", tree)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    tool.load_env()

    assert os.environ["GEMINI_API_KEY"] == "live-key"
    assert os.environ["SETTING"] == "kept"      # settings still load
    assert "GEMINI_API_KEY ignored" in capsys.readouterr().err


def test_env_file_settings_beat_the_environment(tool, tmp_path, monkeypatch):
    tree = tmp_path / "tree"
    tree.mkdir()
    write_env(tree / ".env", "SETTING=from-file\n")
    monkeypatch.setenv("SETTING", "from-shell")
    monkeypatch.setattr(tool, "SCRIPT_DIR", tree)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)

    tool.load_env()

    assert os.environ["SETTING"] == "from-file"


def test_pointer_at_a_missing_file_stops_the_run(tool, tmp_path, monkeypatch):
    monkeypatch.setenv(tool.SECRETS_POINTER, str(tmp_path / "absent"))
    no_tree(tool, tmp_path, monkeypatch)
    with pytest.raises(SystemExit) as e:
        tool.load_env()
    assert "does not exist" in str(e.value)


def test_loose_vault_permissions_are_reported_not_fatal(tool, tmp_path, monkeypatch, capsys):
    vault = write_env(tmp_path / "env", "GEMINI_API_KEY=live-key\n", mode=0o644)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", vault)
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    no_tree(tool, tmp_path, monkeypatch)

    tool.load_env()

    assert os.environ["GEMINI_API_KEY"] == "live-key"
    assert "should be 0600" in capsys.readouterr().err


# ─── require_key ─────────────────────────────────────────────────────────────

def test_missing_key_names_the_vault_file(tool, tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv(tool.SECRETS_POINTER, raising=False)
    monkeypatch.setattr(tool, "DEFAULT_SECRETS_PATH", tmp_path / "absent")
    with pytest.raises(SystemExit) as e:
        tool.require_key()
    msg = str(e.value)
    assert str(tmp_path / "absent") in msg and " env` shows what was found" in msg


def test_present_key_passes_quietly(tool, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "anything")
    assert tool.require_key() is None
