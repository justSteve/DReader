import subprocess

import pytest

import cuts


def test_parse_box():
    assert cuts.parse_box("10,20,300,200") == (10, 20, 300, 200)


@pytest.mark.parametrize("bad", ["10,20,300", "a,b,c,d", "10,20,0,200", "-1,0,10,10"])
def test_parse_box_rejects(bad):
    with pytest.raises(SystemExit, match="--crop"):
        cuts.parse_box(bad)


def test_crop_command_and_output_name(tmp_path):
    cmd, out = cuts.crop_command(tmp_path / "shot.png", (10, 20, 300, 200), tmp_path / "crops")
    assert out == tmp_path / "crops" / "crop-10-20-300x200.png"
    assert cmd[cmd.index("-vf") + 1] == "crop=300:200:10:20"


def test_audio_cut_command_uses_a_duration_not_an_end(tmp_path):
    cmd, out = cuts.audio_cut_command(tmp_path / "ep.m4a", 90, 150, tmp_path / "chunks")
    assert out == tmp_path / "chunks" / "chunk-90-150.m4a"
    assert cmd[cmd.index("-ss") + 1] == "90" and cmd[cmd.index("-t") + 1] == "60"
    assert cmd.index("-ss") < cmd.index("-i")


def test_crop_really_crops(tmp_path):
    src = tmp_path / "shot.png"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=640x480",
                    "-frames:v", "1", str(src)], check=True)
    out = cuts.crop(src, (10, 20, 300, 200), tmp_path / "crops")
    assert cuts.image_size(out) == (300, 200)
