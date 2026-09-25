"""Local ffmpeg cuts: the zoom step for kinds Gemini cannot window itself."""
import re
import subprocess
import sys


def parse_box(s):
    m = re.fullmatch(r"\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*", s or "")
    if not m or int(m.group(3)) == 0 or int(m.group(4)) == 0:
        sys.exit(f"--crop wants X,Y,W,H in pixels (W and H > 0), got {s!r}")
    return tuple(int(g) for g in m.groups())


def crop_command(src, box, out_dir):
    x, y, w, h = box
    out = out_dir / f"crop-{x}-{y}-{w}x{h}.png"
    return ["ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-vf", f"crop={w}:{h}:{x}:{y}", "-frames:v", "1", str(out)], out


def crop(src, box, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = crop_command(src, box, out_dir)
    subprocess.run(cmd, check=True, timeout=120)
    return out


def audio_cut_command(src, a, b, out_dir):
    # -ss and -t as INPUT options: seek, then read b-a seconds. A stream copy
    # needs no re-encode; the cut lands on the nearest frame (tens of ms).
    out = out_dir / f"chunk-{a}-{b}{src.suffix.lower()}"
    return ["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-t", str(b - a),
            "-i", str(src), "-c", "copy", str(out)], out


def cut_audio(src, a, b, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = audio_cut_command(src, a, b, out_dir)
    if not out.exists():
        subprocess.run(cmd, check=True, timeout=120)
    return out


def image_size(path):
    """(width, height) via ffprobe; (0, 0) if it cannot tell."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True, timeout=30).stdout.strip()
        w, h = out.split(",")[:2]
        return int(w), int(h)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            ValueError, FileNotFoundError):
        return 0, 0
