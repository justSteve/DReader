"""Audio path (dr-dqm.2, B4 review): paid replies are archived before any
re-basing, re-basing never raises, windows clamp to the file, re-fetch is safe."""
import argparse
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

import perceive
import prompts
import sources
from sources import Source


# ---------------------------------------------------------- rebase_claims ----

def test_rebase_claims_rebases_good_timestamps():
    payload = {"claims": [{"t": "0:05"}, {"t": "1:10"}, {"t": None}, {"t": 7}]}
    perceive.rebase_claims(payload, 90)
    assert [c["t"] for c in payload["claims"]] == ["1:35", "2:40", None, "1:37"]
    assert "uncertainties" not in payload


@pytest.mark.parametrize("bad", ["about 0:05", "1:10-1:20", 5.5, "1:2:3:4", "x", True])
def test_rebase_claims_keeps_an_unparseable_t_and_says_so(bad):
    payload = {"claims": [{"t": bad}, {"t": "0:05"}]}
    perceive.rebase_claims(payload, 60)
    assert payload["claims"][0]["t"] == bad
    assert payload["claims"][1]["t"] == "1:05"
    assert payload["uncertainties"] == [
        f"t {bad!r} not re-based (clip-relative; offset 60s)"]


def test_rebase_claims_appends_to_existing_uncertainties():
    payload = {"claims": [{"t": "soon"}], "uncertainties": ["muffled at 0:20"]}
    perceive.rebase_claims(payload, 30)
    assert payload["uncertainties"] == [
        "muffled at 0:20", "t 'soon' not re-based (clip-relative; offset 30s)"]


def test_rebase_claims_notes_a_claim_that_is_not_an_object():
    payload = {"claims": ["1:10 he says 4302", {"t": "0:01"}]}
    perceive.rebase_claims(payload, 60)
    assert payload["claims"][0] == "1:10 he says 4302"
    assert payload["claims"][1]["t"] == "1:01"
    assert len(payload["uncertainties"]) == 1
    assert "not re-based" in payload["uncertainties"][0]


@pytest.mark.parametrize("payload", [[{"t": "0:05"}], "text", None,
                                     {"claims": "0:05"}, {"claims": None}])
def test_rebase_claims_never_raises_on_odd_shapes(payload):
    perceive.rebase_claims(payload, 60)


# -------------------------------------------------------------- harness ----

@pytest.fixture
def audio_src(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")
    f = tmp_path / "ep.m4a"
    f.write_bytes(b"x")
    d = sources.dossier_dir("ep-test")
    card = d / "CARD.md"
    card.write_text("# Media: ep-test\n\n## Run log\n")
    src = Source(kind="audio", id="ep-test", card=card, path=f, mime="audio/mp4")
    monkeypatch.setattr(perceive, "resolve_source", lambda args: src)
    monkeypatch.setattr(perceive.creds, "require_key", lambda who: None)
    cut_calls = []

    def cut(path, a, b, out_dir):
        cut_calls.append((a, b))
        return tmp_path / f"chunk-{a}-{b}.m4a"
    monkeypatch.setattr(perceive.cuts, "cut_audio", cut)
    monkeypatch.setattr(perceive, "media_part", lambda *a, **k: "PART")
    from google import genai
    monkeypatch.setattr(genai, "Client", lambda: object())
    from google.genai import types
    monkeypatch.setattr(types, "Content", lambda parts: parts)
    monkeypatch.setattr(types, "Part", lambda text: text)
    replies = []

    def gen(client, model, contents, config):
        return model, SimpleNamespace(text=replies.pop(0), usage_metadata=None)
    monkeypatch.setattr(perceive.gemini, "generate_with_retry", gen)
    monkeypatch.setattr(perceive.gemini, "media_config", lambda *a, **k: None)
    return SimpleNamespace(src=src, dir=d, replies=replies, cuts=cut_calls)


def ask_args(**kw):
    base = dict(file=None, id="ep-test", url=None, question="numbers?", start=None,
                end=None, fps=None, resolution=None, crop=None, model="m")
    base.update(kw)
    return argparse.Namespace(**base)


def tr_args(**kw):
    base = dict(file=None, id="ep-test", url=None, start=None, end=None, chunk=1.0,
                fps=None, resolution=None, absolute=False, model="m")
    base.update(kw)
    return argparse.Namespace(**base)


def only_run(d):
    (run,) = sorted((d / "runs").iterdir())
    return run


# ------------------------------------------------------------ ask window ----

def test_ask_archives_the_raw_reply_before_re_basing(audio_src, monkeypatch, capsys):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 600)
    audio_src.replies.append(json.dumps(
        {"summary": "s", "claims": [{"t": "0:05"}, {"t": "about 0:10"}]}))
    perceive.cmd_ask(ask_args(start="1:00", end="1:40"))
    run = only_run(audio_src.dir)
    raw = json.loads((run / "response.json").read_text())
    rebased = json.loads((run / "response.rebased.json").read_text())
    assert [c["t"] for c in raw["claims"]] == ["0:05", "about 0:10"]
    assert [c["t"] for c in rebased["claims"]] == ["1:05", "about 0:10"]
    assert "offset 60s" in rebased["uncertainties"][0]
    assert json.loads((run / "request.json").read_text())["offset_s"] == 60
    printed = capsys.readouterr().out
    assert json.loads(printed)["claims"][0]["t"] == "1:05"


def test_ask_without_a_window_writes_no_rebased_copy(audio_src):
    audio_src.replies.append(json.dumps({"summary": "s", "claims": [{"t": "0:05"}]}))
    perceive.cmd_ask(ask_args())
    run = only_run(audio_src.dir)
    assert not (run / "response.rebased.json").exists()
    assert json.loads((run / "request.json").read_text())["offset_s"] == 0


def test_ask_window_clamps_end_to_the_duration(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 100)
    audio_src.replies.append(json.dumps({"summary": "s", "claims": []}))
    perceive.cmd_ask(ask_args(start="1:00", end="5:00"))
    assert audio_src.cuts == [(60, 100)]


def test_ask_window_refuses_a_start_past_the_end(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 100)
    with pytest.raises(SystemExit, match=r"--start 2:00 is at or past the end \(1:40\)"):
        perceive.cmd_ask(ask_args(start="2:00"))
    assert audio_src.cuts == []


def test_ask_window_says_duration_unknown_only_when_it_is(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 0)
    with pytest.raises(SystemExit, match=r"\(duration unknown\)"):
        perceive.cmd_ask(ask_args(start="1:00"))
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 600)
    with pytest.raises(SystemExit) as e:
        perceive.cmd_ask(ask_args(start="2:00", end="1:00"))
    assert "duration unknown" not in str(e.value.code)
    assert "--end after --start" in str(e.value.code)


# ------------------------------------------------------ transcribe_audio ----

def test_transcribe_audio_archives_raw_and_records_offset(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 100)
    audio_src.replies += [
        json.dumps({"segments": [{"t": "0:05", "speech": "a"}]}),
        json.dumps({"segments": [{"t": "0:02", "speech": "b"},
                                 {"t": "about 0:30", "speech": "c"}]}),
    ]
    perceive.transcribe_audio(tr_args(), audio_src.src)
    assert audio_src.cuts == [(0, 60), (60, 100)]
    r1, r2 = sorted((audio_src.dir / "runs").iterdir())
    assert json.loads((r2 / "request.json").read_text())["offset_s"] == 60
    assert json.loads((r1 / "request.json").read_text())["offset_s"] == 0
    raw2 = json.loads((r2 / "response.json").read_text())
    assert [s["t"] for s in raw2["segments"]] == ["0:02", "about 0:30"]
    out = json.loads((audio_src.dir / "transcript.json").read_text())
    assert [s["t"] for s in out["segments"]] == ["0:05", "1:02", "about 0:30"]
    assert any("about 0:30" in u for u in out["uncertainties"])
    assert out["speaker_labels"].startswith("per chunk")


def test_transcribe_audio_clamps_end_and_refuses_start_past_end(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 100)
    with pytest.raises(SystemExit, match=r"--start 2:00 is at or past the end \(1:40\)"):
        perceive.transcribe_audio(tr_args(start="2:00"), audio_src.src)
    audio_src.replies.append(json.dumps({"segments": []}))
    perceive.transcribe_audio(tr_args(start="1:00", end="9:00"), audio_src.src)
    assert audio_src.cuts == [(60, 100)]


def test_transcribe_audio_empty_window_leaves_transcript_untouched(audio_src, monkeypatch):
    monkeypatch.setattr(perceive, "probe_duration", lambda p: 600)
    tj = audio_src.dir / "transcript.json"
    tj.write_text('{"keep": true}')
    with pytest.raises(SystemExit, match="empty window"):
        perceive.transcribe_audio(tr_args(start="2:00", end="1:00"), audio_src.src)
    assert tj.read_text() == '{"keep": true}'
    assert not (audio_src.dir / "runs").exists()
    assert audio_src.cuts == []


# ---------------------------------------------------------------- prompts ----

def test_audio_prompts_ask_for_digits_and_honest_speaker_labels():
    for p in (prompts.AUDIO_TRANSCRIBE_PROMPT, prompts.ask_prompt("audio", "q")):
        assert "Write numbers as digits (4302, not four three oh two)." in p
    assert "Keep speaker labels consistent" not in prompts.AUDIO_TRANSCRIBE_PROMPT
    assert "otherwise label Speaker 1, Speaker 2 within this recording" \
        in prompts.AUDIO_TRANSCRIBE_PROMPT
    assert "Write numbers as digits" not in prompts.ask_prompt("document", "q")


# ------------------------------------------------------------------ fetch ----

@pytest.fixture
def fetch_env(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")
    monkeypatch.setattr(sources, "probe_duration", lambda p: 0)
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        if Path(cmd[0]).name != "yt-dlp":
            raise AssertionError(f"unexpected command {cmd}")
        assert "--force-overwrites" in cmd
        assert cmd[cmd.index("--print") + 1] == "after_move:filepath"
        assert kw.get("capture_output") and kw.get("check")
        out = Path(cmd[cmd.index("-o") + 1].replace("%(ext)s", "m4a"))
        out.write_bytes(b"audio")
        return subprocess.CompletedProcess(cmd, 0, stdout=f"\n{out}\n\n", stderr="")
    monkeypatch.setattr(perceive.subprocess, "run", fake_run)
    return SimpleNamespace(dir=tmp_path / "dossiers" / "pod-ep", calls=calls)


def fetch_args(url, id="pod-ep"):
    return argparse.Namespace(url=url, id=id)


def test_fetch_uses_the_path_yt_dlp_prints(fetch_env):
    perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
    rec = json.loads((fetch_env.dir / "source.json").read_text())
    assert rec == {"path": str(fetch_env.dir / "source.m4a"),
                   "origin": "https://pod.example/ep1"}
    assert (fetch_env.dir / "CARD.md").exists()


def test_fetch_new_url_replaces_the_old_audio(fetch_env, capsys):
    perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
    stale = fetch_env.dir / "source.mp3"
    stale.write_bytes(b"old")
    perceive.cmd_fetch(fetch_args("https://pod.example/ep2"))
    assert not stale.exists()
    assert (fetch_env.dir / "source.json").exists()
    rec = json.loads((fetch_env.dir / "source.json").read_text())
    assert rec["origin"] == "https://pod.example/ep2"
    assert ("[pod-ep: replacing audio from https://pod.example/ep1 with "
            "https://pod.example/ep2]") in capsys.readouterr().err


def test_fetch_same_url_keeps_other_files(fetch_env, capsys):
    perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
    other = fetch_env.dir / "source.mp3"
    other.write_bytes(b"x")
    perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
    assert other.exists()
    assert "replacing audio" not in capsys.readouterr().err


def test_fetch_refuses_a_dossier_holding_another_kind(fetch_env, tmp_path):
    fetch_env.dir.mkdir(parents=True)
    video = tmp_path / "cap.mp4"
    video.write_bytes(b"v")
    (fetch_env.dir / "source.json").write_text(
        json.dumps({"path": str(video), "origin": None}))
    with pytest.raises(SystemExit, match="already holds a video"):
        perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
    assert fetch_env.calls == []


def test_fetch_reports_yt_dlp_failure_cleanly(fetch_env, monkeypatch):
    def fail(cmd, **kw):
        raise subprocess.CalledProcessError(
            1, cmd, output="", stderr="line1\nERROR: Unsupported URL: nope\n")
    monkeypatch.setattr(perceive.subprocess, "run", fail)
    with pytest.raises(SystemExit) as e:
        perceive.cmd_fetch(fetch_args("nope"))
    assert "yt-dlp failed" in str(e.value.code)
    assert "Unsupported URL: nope" in str(e.value.code)


def test_fetch_reports_missing_yt_dlp_cleanly(fetch_env, monkeypatch):
    def missing(cmd, **kw):
        raise FileNotFoundError(cmd[0])
    monkeypatch.setattr(perceive.subprocess, "run", missing)
    with pytest.raises(SystemExit, match="yt-dlp not found"):
        perceive.cmd_fetch(fetch_args("https://pod.example/ep1"))
