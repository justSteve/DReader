"""Local ffmpeg cuts: the zoom step for kinds Gemini cannot window itself."""
import hashlib
import os
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
    # format=rgba before crop: on a 4:2:0 source (most screenshots/JPEGs),
    # cropping straight off the chroma-subsampled planes silently rounds an
    # odd width/height down to the nearest even number. rgb24 fixed that but
    # flattened any transparent PNG to opaque black; rgba fixes the rounding
    # the same way while keeping the alpha channel intact.
    return ["ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-vf", f"format=rgba,crop={w}:{h}:{x}:{y}", "-frames:v", "1", str(out)], out


def crop(src, box, out_dir):
    x, y, w, h = box
    W, H = image_size(src)
    if W and H and (x + w > W or y + h > H):
        sys.exit(f"--crop {x},{y},{w},{h} falls outside the {W}×{H} image")
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = crop_command(src, box, out_dir)
    subprocess.run(cmd, check=True, timeout=120)
    return out


def audio_cut_command(src, a, b, out_dir):
    # -ss and -t as INPUT options: seek, then read b-a seconds. A stream copy
    # needs no re-encode for most containers; the cut lands on the nearest
    # frame (tens of ms). FLAC is the exception: copying a mid-stream slice
    # leaves the STREAMINFO header's duration pointing at the original file,
    # so FLAC chunks are re-encoded instead.
    suffix = src.suffix.lower()
    st = src.stat()
    tag = hashlib.sha1(
        f"{st.st_size}:{st.st_mtime_ns}:{src.resolve()}".encode()).hexdigest()[:10]
    out = out_dir / f"chunk-{a}-{b}-{tag}{suffix}"
    codec = ["-c:a", "flac"] if suffix == ".flac" else ["-c", "copy"]
    return ["ffmpeg", "-y", "-v", "error", "-ss", str(a), "-t", str(b - a),
            "-i", str(src), *codec, str(out)], out


def cut_audio(src, a, b, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd, out = audio_cut_command(src, a, b, out_dir)
    if out.exists():
        return out
    # Write to a .part file and rename into place only on success, so a
    # chunk that dies partway through never leaves a same-named file behind
    # for the out.exists() fast path above to mistake for a finished cut.
    part = out.with_name(out.stem + ".part" + out.suffix)
    cmd = cmd[:-1] + [str(part)]
    try:
        subprocess.run(cmd, check=True, timeout=120)
        os.replace(part, out)
    except Exception:
        part.unlink(missing_ok=True)
        raise
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
