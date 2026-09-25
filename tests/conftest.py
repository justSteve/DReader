"""Put the repo root (for dreader_core) and the media tool's directory (for
its modules, from Task 7 on) on sys.path. The tools do the same for
themselves at import time, so tests and tools resolve the same module objects."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for p in (REPO_ROOT, REPO_ROOT / "media-reader"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
