"""Neither tool may carry a private copy of what dreader_core holds [dr-dqm.1].

The copies drifted before: dread.py kept a retired fallback model, no
transport-error retry and no empty-reply guard for weeks after yta.py fixed
all three. This test fails when a copy grows back — by name (PRIVATE_COPIES)
or by content (MARKERS)."""
import importlib.util
import sys
from pathlib import Path

import pytest

import dreader_core.creds

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "media": [REPO_ROOT / "media-reader" / "mread.py", REPO_ROOT / "yt-analyst" / "yta.py"],
    "dread": [REPO_ROOT / "discord-reader" / "dread.py"],
}
PRIVATE_COPIES = ["parse_env_file", "secrets_path", "load_env", "require_key",
                  "SECRETS_POINTER", "DEFAULT_SECRETS_PATH",
                  "report_env", "SECRET_NAMES", "MODELS_URL"]

# Literals only a private copy of the shared logic would contain, whatever
# it is named. Tasks 3-4 extend this list as more moves into dreader_core.
# NOTE: "/home/vault" alone also matches the module docstring's "Requires:"
# line on both tools (a legitimate mention of where the vault lives), so the
# marker is narrowed to the constructor shape the deleted constant used.
MARKERS = ["Path(\"/home/vault", "DREADER_SECRETS_FILE", "x-goog-api-key",
           "os.environ.update(", "hashlib.sha256(key"]


@pytest.fixture(params=sorted(TOOLS), ids=sorted(TOOLS))
def tool(request):
    path = next((p for p in TOOLS[request.param] if p.exists()), None)
    assert path, f"no script found among {TOOLS[request.param]}"
    name = f"{request.param}_under_test"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    yield mod
    del sys.modules[name]


@pytest.mark.parametrize("name", PRIVATE_COPIES)
def test_no_private_copy(tool, name):
    assert not hasattr(tool, name), f"{tool.__name__} defines its own {name}"


@pytest.mark.parametrize("marker", MARKERS)
def test_no_private_logic(tool, marker):
    src = Path(tool.__file__).read_text()
    assert marker not in src, f"{Path(tool.__file__).name} contains {marker!r} — use dreader_core"


def test_uses_the_shared_creds(tool):
    assert tool.creds is dreader_core.creds
