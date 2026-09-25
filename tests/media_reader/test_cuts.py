from pathlib import Path

import subprocess

import pytest

import cuts
import perceive


def test_parse_box():
    assert cuts.parse_box("10,20,300,200") == (10, 20, 300, 200)


@pytest.mark.parametrize("bad", ["10,20,300", "a,b,c,d", "10,20,0,200", "-1,0,10,10"])
def test_parse_box_rejects(bad):
    with pytest.raises(SystemExit, match="--crop"):
        cuts.parse_box(bad)


def test_crop_command_and_output_name(tmp_path):
    cmd, out = cuts.crop_command(tmp_path / "shot.png", (10, 20, 300, 200), tmp_path / "crops")
    assert out == tmp_path / "crops" / "crop-10-20-300x200.png"
    assert cmd[cmd.index("-vf") + 1] == "format=rgb24,crop=300:200:10:20"


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
