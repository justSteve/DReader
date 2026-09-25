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
