from pathlib import Path

import hashlib
import subprocess

import pytest

import cuts
import perceive


def pix_fmt(path):
    return subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=pix_fmt", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()


def test_parse_box():
    assert cuts.parse_box("10,20,300,200") == (10, 20, 300, 200)


@pytest.mark.parametrize("bad", ["10,20,300", "a,b,c,d", "10,20,0,200", "-1,0,10,10"])
def test_parse_box_rejects(bad):
    with pytest.raises(SystemExit, match="--crop"):
        cuts.parse_box(bad)


def test_crop_command_and_output_name(tmp_path):
    cmd, out = cuts.crop_command(tmp_path / "shot.png", (10, 20, 300, 200), tmp_path / "crops")
    assert out == tmp_path / "crops" / "crop-10-20-300x200.png"
    assert cmd[cmd.index("-vf") + 1] == "format=rgba,crop=300:200:10:20"


def test_audio_cut_command_uses_a_duration_not_an_end(tmp_path):
    src = tmp_path / "ep.m4a"
    src.write_bytes(b"x")
    cmd, out = cuts.audio_cut_command(src, 90, 150, tmp_path / "chunks")
    assert out.parent == tmp_path / "chunks"
    assert out.name.startswith("chunk-90-150-") and out.name.endswith(".m4a")
    assert cmd[cmd.index("-ss") + 1] == "90" and cmd[cmd.index("-t") + 1] == "60"
    assert cmd.index("-ss") < cmd.index("-i")
    assert cmd[cmd.index("-c") + 1] == "copy"


def test_audio_cut_command_chunk_name_is_keyed_to_the_source(tmp_path):
    a = tmp_path / "a.m4a"
    a.write_bytes(b"x")
    b = tmp_path / "b.m4a"
    b.write_bytes(b"yy")
    _, out_a = cuts.audio_cut_command(a, 0, 60, tmp_path / "chunks")
    _, out_b = cuts.audio_cut_command(b, 0, 60, tmp_path / "chunks")
    assert out_a != out_b


def test_audio_cut_command_chunk_tag_hashes_size_mtime_and_path(tmp_path):
    src = tmp_path / "ep.m4a"
    src.write_bytes(b"hello world")
    st = src.stat()
    expected = hashlib.sha1(
        f"{st.st_size}:{st.st_mtime_ns}:{src.resolve()}".encode()).hexdigest()[:10]
    _, out = cuts.audio_cut_command(src, 0, 60, tmp_path / "chunks")
    assert out.name == f"chunk-0-60-{expected}.m4a"


def test_audio_cut_command_reencodes_flac(tmp_path):
    src = tmp_path / "ep.flac"
    src.write_bytes(b"x")
    cmd, out = cuts.audio_cut_command(src, 0, 60, tmp_path / "chunks")
    assert cmd[cmd.index("-c:a") + 1] == "flac"
    assert "copy" not in cmd


def test_crop_really_crops(tmp_path):
    src = tmp_path / "shot.png"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=640x480",
                    "-frames:v", "1", str(src)], check=True)
    out = cuts.crop(src, (10, 20, 300, 200), tmp_path / "crops")
    assert cuts.image_size(out) == (300, 200)


def test_crop_rejects_a_box_outside_the_image(tmp_path):
    src = tmp_path / "shot.png"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=256x64",
                    "-frames:v", "1", str(src)], check=True)
    with pytest.raises(SystemExit, match="256×64"):
        cuts.crop(src, (200, 0, 100, 10), tmp_path / "crops")
    out = cuts.crop(src, (0, 0, 256, 64), tmp_path / "crops")
    assert cuts.image_size(out) == (256, 64)


def test_crop_handles_odd_sizes_on_a_chroma_subsampled_jpeg(tmp_path):
    src = tmp_path / "shot.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=green:s=256x64",
                    "-frames:v", "1", "-pix_fmt", "yuvj420p", str(src)], check=True)
    out = cuts.crop(src, (13, 3, 101, 11), tmp_path / "crops")
    assert cuts.image_size(out) == (101, 11)


def test_crop_keeps_alpha_on_a_transparent_png(tmp_path):
    # A 64x64 fully-transparent canvas with a 16x16 opaque black square
    # drawn at (24,24). format=rgb24 would flatten the transparent area to
    # solid black; format=rgba must keep it transparent.
    src = tmp_path / "shot.png"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi",
                    "-i", "color=c=black@0.0:s=64x64",
                    "-vf", "format=rgba,drawbox=x=24:y=24:w=16:h=16:color=black@1.0:t=fill",
                    "-frames:v", "1", str(src)], check=True)
    assert pix_fmt(src) == "rgba"
    over_square = cuts.crop(src, (24, 24, 16, 16), tmp_path / "crops")
    over_empty = cuts.crop(src, (0, 0, 16, 16), tmp_path / "crops")
    assert pix_fmt(over_square) == "rgba"
    assert pix_fmt(over_empty) == "rgba"


def test_cut_audio_writes_atomically_and_cleans_up_on_failure(tmp_path, monkeypatch):
    src = tmp_path / "ep.m4a"
    src.write_bytes(b"x")
    out_dir = tmp_path / "chunks"
    _, out = cuts.audio_cut_command(src, 0, 60, out_dir)

    def boom(cmd, **kw):
        Path(cmd[-1]).write_bytes(b"partial")
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(cuts.subprocess, "run", boom)
    with pytest.raises(subprocess.CalledProcessError):
        cuts.cut_audio(src, 0, 60, out_dir)
    assert not out.exists()
    assert not list(out_dir.glob("*.part*"))

    def ok(cmd, **kw):
        Path(cmd[-1]).write_bytes(b"done")

    monkeypatch.setattr(cuts.subprocess, "run", ok)
    result = cuts.cut_audio(src, 0, 60, out_dir)
    assert result == out and out.exists() and out.read_bytes() == b"done"
    assert not list(out_dir.glob("*.part*"))


def test_window_label():
    assert perceive.window_label(None, None, None) == " [full]"
    assert perceive.window_label("01:00", None, None) == " [01:00-end]"
    assert perceive.window_label(None, "02:00", None) == " [0:00-02:00]"
    assert perceive.window_label(None, None, "250,50,1500,120") == " [crop 250,50,1500,120]"


def test_audio_claims_are_rebased_to_file_time():
    payload = {"claims": [{"t": "0:05"}, {"t": "1:10"}, {"t": None}]}
    perceive.rebase_claims(payload, 90)
    assert [c["t"] for c in payload["claims"]] == ["1:35", "2:40", None]


class _KeyReached(Exception):
    pass


def _audio_ask_args(tmp_path, **kw):
    import argparse
    audio = tmp_path / "ep.m4a"
    audio.write_bytes(b"x")
    base = dict(file=str(audio), id="audio-guard-test", url=None, question="q",
                start=None, end=None, fps=None, resolution=None, crop=None,
                model="m")
    base.update(kw)
    return argparse.Namespace(**base)


def _fake_source(monkeypatch, tmp_path):
    import sources
    from sources import Source
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")
    src = Source(kind="audio", id="audio-guard-test", card=tmp_path / "CARD.md",
                 path=tmp_path / "ep.m4a", mime="audio/mp4")
    monkeypatch.setattr(perceive, "resolve_source", lambda args: src)

    def key(_who):
        raise _KeyReached()
    monkeypatch.setattr(perceive.creds, "require_key", key)
    cut_calls = []
    monkeypatch.setattr(perceive.cuts, "cut_audio",
                        lambda *a, **k: cut_calls.append(a) or tmp_path / "chunk.m4a")
    return cut_calls


def test_audio_ask_refuses_fps_before_the_key(tmp_path, monkeypatch):
    _fake_source(monkeypatch, tmp_path)
    with pytest.raises(SystemExit, match="no frames"):
        perceive.cmd_ask(_audio_ask_args(tmp_path, fps=2.0))


def test_audio_ask_window_passes_the_guard(tmp_path, monkeypatch):
    cut_calls = _fake_source(monkeypatch, tmp_path)
    with pytest.raises(_KeyReached):
        perceive.cmd_ask(_audio_ask_args(tmp_path, start="1:00", end="1:40"))
    assert [c[1:3] for c in cut_calls] == [(60, 100)]


def test_audio_ask_window_refuses_end_before_start(tmp_path, monkeypatch):
    _fake_source(monkeypatch, tmp_path)
    with pytest.raises(SystemExit, match="--end after --start"):
        perceive.cmd_ask(_audio_ask_args(tmp_path, start="1:40", end="1:00"))
