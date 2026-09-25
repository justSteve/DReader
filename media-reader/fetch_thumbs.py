#!/usr/bin/env python3
"""Fetch each video's YouTube cover image into videos/<id>/thumb.jpg, downscaled
to 640px wide (JPEG q72, ~30 KB) so build_reader.py can inline it — the
published page cannot load images from the network. Skips files that exist.

  python3 fetch_thumbs.py [--force]
"""
import io, sys, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
force = "--force" in sys.argv
done = skipped = failed = 0
for vdir in sorted(p for p in (ROOT / "videos").iterdir() if p.is_dir()):
    out = vdir / "thumb.jpg"
    if out.exists() and not force:
        skipped += 1
        continue
    data = None
    for name in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            with urllib.request.urlopen(f"https://i.ytimg.com/vi/{vdir.name}/{name}.jpg", timeout=20) as r:
                data = r.read()
            if len(data) > 2000:      # YouTube serves a tiny grey placeholder for missing sizes
                break
        except Exception:
            data = None
    if not data:
        print("failed", vdir.name); failed += 1; continue
    im = Image.open(io.BytesIO(data)).convert("RGB")
    # hqdefault is 4:3 with letterbox bars; crop to 16:9
    w, h = im.size
    if abs(w / h - 16 / 9) > 0.05:
        nh = round(w * 9 / 16); top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    im.thumbnail((640, 360))
    im.save(out, "JPEG", quality=72, optimize=True, progressive=True)
    done += 1
print(f"thumbs: {done} fetched, {skipped} present, {failed} failed")
