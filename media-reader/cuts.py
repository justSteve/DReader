"""Local ffmpeg cuts: the zoom step for kinds Gemini cannot window itself."""
import subprocess


def image_size(path):
    """(width, height) via ffprobe; (0, 0) if it cannot tell."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        w, h = out.split(",")[:2]
        return int(w), int(h)
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return 0, 0
