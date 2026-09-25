"""The vault: where the secret value lives, and how a tool loads it.

Secret values live in one file outside every project tree, mode 0600; the
repo holds a pointer at most. Set DREADER_SECRETS_FILE to read a different
file — that is the only supported override, and it must exist."""
import hashlib
import json
import os
import sys
from pathlib import Path

SECRETS_POINTER = "DREADER_SECRETS_FILE"
DEFAULT_SECRETS_PATH = Path("/home/vault/DReader/env")
SECRET_NAMES = ("GEMINI_API_KEY",)
MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1"


def parse_env_file(path):
    """KEY=VALUE lines from an env file, as a dict. A leading `export `, blank
    lines, `#` comments and surrounding quotes are stripped; anything without an
    `=` is skipped. Later lines win over earlier ones."""
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        if k.startswith("export "):
            k = k[len("export "):].strip()
        if not k:
            continue
        values[k] = v.strip().strip('"').strip("'")
    return values


def secrets_path():
    """Which vault file to read, and whether it was named explicitly.

    Explicit (``DREADER_SECRETS_FILE`` in the environment): that path, and it
    must exist. Implicit: the default vault path, only if it is there.
    ``(None, False)`` means there is no vault file to read."""
    raw = os.environ.get(SECRETS_POINTER)
    if raw:
        return Path(raw).expanduser(), True
    if DEFAULT_SECRETS_PATH.exists():
        return DEFAULT_SECRETS_PATH, False
    return None, False


def load_env(tool_dir):
    """Populate ``os.environ`` from the vault file and the local ``.env``.

    Precedence is vault file > ``.env`` > the process environment. A file value
    OVERWRITES what the shell exported — that direction is the whole point: on
    2026-09-05 every shell still carried a dead April GEMINI_API_KEY, and the
    old ``setdefault`` let it shadow the live key, so every call came back
    ``API key not valid`` [co-yuyh9]. Secret names are refused from the in-tree
    ``.env`` outright; their values live in the vault, outside every project
    tree (credential estate convention, 2026-08-25). ``tool_dir`` is the
    directory whose ``.env`` holds the tool's non-secret settings
    (DREAD_CAPTURE_DIR, for one)."""
    values = {}

    env_path = Path(tool_dir) / ".env"
    if env_path.exists():
        for k, v in parse_env_file(env_path).items():
            if k in SECRET_NAMES:
                print(f"[{env_path.name}: {k} ignored — a secret value belongs in "
                      f"{DEFAULT_SECRETS_PATH}, not in the tree]", file=sys.stderr)
                continue
            values[k] = v

    path, explicit = secrets_path()
    if path is not None:
        if not path.exists():
            sys.exit(f"{SECRETS_POINTER} names {path}, which does not exist.")
        mode = path.stat().st_mode & 0o777
        if mode & 0o077:
            print(f"[{path} is mode {mode:04o}; a vault file should be 0600]",
                  file=sys.stderr)
        values.update(parse_env_file(path))

    os.environ.update(values)

    # This tool's credential is GEMINI_API_KEY, full stop. An ambient
    # GOOGLE_API_KEY must never shadow it — evict it for this process.
    if os.environ.get("GEMINI_API_KEY"):
        os.environ.pop("GOOGLE_API_KEY", None)


def require_key(tool):
    """Exit with the one instruction that fixes it, naming the vault file."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    path, _ = secrets_path()
    where = path or DEFAULT_SECRETS_PATH
    sys.exit(f"GEMINI_API_KEY not set: add the line to {where} (mode 0600), "
             f"or point {SECRETS_POINTER} at the vault file that holds it. "
             f"`{tool} env` shows what was found.")


def report_env(tool_dir, tool, no_check):
    """Say where the credential came from and whether Google still accepts it.
    Never prints the value — length and a sha256 prefix are enough to tell two
    keys apart, which is the question this answers."""
    import urllib.error
    import urllib.request

    path, explicit = secrets_path()
    origin = f" (named by {SECRETS_POINTER})" if explicit else ""
    print(f"vault file : {path if path else '(none found)'}{origin}")
    local = Path(tool_dir) / ".env"
    print(f"local .env : {local if local.exists() else '(none — correct)'}")

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        require_key(tool)
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    print(f"credential : GEMINI_API_KEY, {len(key)} chars, sha256:{digest}")

    if no_check:
        return
    req = urllib.request.Request(MODELS_URL, headers={"x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"live check : HTTP {r.status} — the key authenticates")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail)["error"]["message"]
        except Exception:
            detail = detail[:200]
        sys.exit(f"live check : HTTP {e.code} — {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"live check : no answer from Google — {e.reason}")
