"""Gemini Files API: upload once, reuse the handle for 48 h."""
import json
import sys
import time
from datetime import datetime

UPLOAD_TTL_S = 47 * 3600  # Files API keeps an upload 48 h; leave a margin


def upload_file(client, path, mime_type=None):
    """Upload and wait until ACTIVE. No cache — dread.py deletes its upload
    after one use; media-reader goes through upload_cached."""
    print(f"[uploading {path.name} ({path.stat().st_size / 1e6:.0f} MB)...]",
          file=sys.stderr)
    t0 = time.time()
    f = client.files.upload(file=str(path),
                            config={"mime_type": mime_type} if mime_type else None)
    while f.state.name == "PROCESSING":
        time.sleep(4)
        f = client.files.get(name=f.name)
    if f.state.name != "ACTIVE":
        sys.exit(f"Upload failed: file state {f.state.name}")
    print(f"[upload active: {f.name} in {time.time() - t0:.0f}s]", file=sys.stderr)
    return f


def upload_cached(client, cache, path, mime_type=None):
    """Upload through the Files API once; reuse the handle recorded in `cache`
    (a JSON file) while it is fresh, the same file, and ACTIVE server-side.
    Uploads of ~1 GB take minutes over the WSL bridge; the cache is what makes
    clipped follow-ups near-free."""
    if cache.exists():
        try:
            rec = json.loads(cache.read_text())
            if (rec.get("path") == str(path) and rec.get("size") == path.stat().st_size
                    and rec.get("expires", 0) > time.time() + 300):
                f = client.files.get(name=rec["name"])
                if f.state.name == "ACTIVE":
                    print(f"[upload reused: {f.name}, expires "
                          f"{datetime.fromtimestamp(rec['expires']):%Y-%m-%d %H:%M}]",
                          file=sys.stderr)
                    return f
        except Exception as e:  # stale, expired, deleted server-side
            print(f"[upload cache unusable: {e}; re-uploading]", file=sys.stderr)
    f = upload_file(client, path, mime_type)
    cache.write_text(json.dumps({
        "name": f.name, "uri": f.uri, "mime_type": f.mime_type,
        "path": str(path), "size": path.stat().st_size,
        "uploaded": datetime.now().isoformat(timespec="seconds"),
        "expires": time.time() + UPLOAD_TTL_S,
    }, indent=2))
    return f
