#!/usr/bin/env python3
"""dread.py v0.2 — Discord Reader: screen-captured pages -> Gemini -> transcript.

Workflow:
  1. Focus Discord, CLICK INTO THE MESSAGE PANE, navigate to the start point.
  2. Win+Alt+R starts Game Bar capture of the focused window.
  3. PageDown, hold ~1 second, repeat to the endpoint. (Never press Esc —
     Discord jumps to newest.) Win+Alt+R again to stop.
  4. `dread.py ingest --label "server/channel"` does the rest.

Changes from v0.1:
  - Paging is the capture doctrine (Steve's ruling, 2026-08-28): default
    transcription prompt describes a paged capture with ~1s holds and
    seam-overlap dedup rules. `--mode scroll` retains the old framing as
    fallback. Mode is recorded in the run log.

Subcommands:
  ingest  Pull a capture (newest from the Captures folder, or --file), move it
          into its dossier, upload to Gemini, transcribe messages, render
          transcript.json + transcript.md, create/append CARD.md.
  ask     Follow-up question against an already-ingested capture's video.
  env     Say where the credential came from and whether it still works.

Requires: GEMINI_API_KEY in the vault file /home/vault/DReader/env, mode 0600;
          `pip install google-genai`.
          When a call comes back unauthenticated, run `dread.py env` first.
Optional .env keys (settings only, never secrets):
  DREAD_CAPTURE_DIR  (default /mnt/c/Users/steve/Videos/Captures; on this box
                     the folder is OneDrive-redirected, see .env)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CAPTURES_DIR = SCRIPT_DIR / "captures"

# ─── The vault: where the secret value lives ─────────────────────────────────
# Secret values live in one file outside every project tree, mode 0600; the
# repo holds a pointer at most. Set DREADER_SECRETS_FILE to read a different
# file — that is the only supported override, and it must exist.
SECRETS_POINTER = "DREADER_SECRETS_FILE"
DEFAULT_SECRETS_PATH = Path("/home/vault/DReader/env")
SECRET_NAMES = ("GEMINI_API_KEY",)

MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1"

DEFAULT_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-2.5-flash"]
RETRYABLE = {429, 500, 503}
MAX_ATTEMPTS = 4
BASE_DELAY_S = 5
DEFAULT_FPS = 2.0  # ~1s page holds -> ~2 samples per page, >=1 clean still
# Gemini media_resolution. Measured 2026-09-12 on the uploaded-file path
# (dr-vm0), same 21 s clip: default == low (~63 tok/frame, 3.3k prompt
# tokens); high is ~261 tok/frame (12k). At default Gemini confabulated 4 of 5
# timestamps, dropped the thread's opening message, invented a "Pinned a
# message" entry and read no reply headers; at high all of those were right.
# High is therefore the default: 3.5x tokens on a cheap model buys a
# transcript whose timestamps can be trusted.
RESOLUTIONS = ("default", "low", "high")
DEFAULT_RESOLUTION = "high"

PROMPT_HEADER = {
    "page": """This video is a screen capture of a Discord channel advanced
PAGE BY PAGE with the PageDown key, holding roughly one second on each page
before advancing. Consecutive pages overlap slightly. Structural facts to use:
- A message visible on two consecutive pages is the SAME message — output it once.
- A message cut off at the bottom of one page appears complete near the top of
  the next page — transcribe the complete version, once.
- Within a held page the screen is static; read from the sharpest frames and
  ignore the brief transition blur between pages.""",
    "scroll": """This video is a screen capture of a Discord channel being
scrolled continuously from an earlier point to a later point. Because it
scrolls, every message appears in many frames — reconstruct the stream with
each message exactly once.""",
}

TRANSCRIBE_PROMPT = """{header}

Your job: reconstruct the message stream, each message EXACTLY ONCE, in
chronological order. Return JSON ONLY (no markdown fences, no prose outside
the JSON):

{
  "context": "server/channel names and any date dividers visible on screen",
  "messages": [
    {
      "date": "date this message belongs to, from Discord's date dividers or timestamps, or null",
      "time": "timestamp shown next to the message, verbatim, or null",
      "author": "display name as shown",
      "text": "full message text, verbatim",
      "reply_to": "author of the quoted/replied-to message if shown, else null",
      "reply_to_text": "the first words of the quoted reply preview, verbatim, else null",
      "attachments": "brief description of images/embeds/links, else null"
    }
  ],
  "uncertainties": ["messages or fragments you could not read fully, with approximate position"]
}

Rules:
- Verbatim text; never paraphrase, summarize, or merge messages. Keep emoji
  that are part of the message text (a 🔥 or 🟢 leading a header is text).
- Forum posts: the channel may be a forum whose post opens with a title,
  then the poster's opening message (badge "OP"), then replies. Transcribe
  the title into context and the opening message as the first message.
- Consecutive messages by the same author with no new header are separate
  entries if Discord renders them as separate messages.
- Carry date dividers ("August 27, 2026") into the date field of following
  messages until the next divider.
- If a message is not fully legible on ANY page/frame, put what you have in
  uncertainties rather than guessing.
"""

CARD_TEMPLATE = """# Capture: {capture_id}

- **Label:** {label}
- **Captured/ingested:** {date}
- **Mode:** {mode}
- **Source:** {source_name} ({size_mb:.1f} MB, moved from {origin})
- **Status:** open

## Summary
_(curated by Claude Code: what this capture covers — channel, date range, topic)_

## Findings
_(curated: anything extracted/decided from this transcript, with message refs)_

## Lessons (this capture)
_(capture-specific: paging-cadence problems, layout quirks, seam-dedup issues)_

## Run log
_(machine-appended by dread.py — do not edit entries)_
"""


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


def load_env():
    """Populate ``os.environ`` from the vault file and the local ``.env``.

    Precedence is vault file > ``.env`` > the process environment. A file value
    OVERWRITES what the shell exported — that direction is the whole point: on
    2026-09-05 every shell still carried a dead April GEMINI_API_KEY, and the
    old ``setdefault`` let it shadow the live key, so every call came back
    ``API key not valid`` [co-yuyh9]. Secret names are refused from the in-tree
    ``.env`` outright; their values live in the vault, outside every project
    tree (credential estate convention, 2026-08-25). Settings such as
    ``DREAD_CAPTURE_DIR`` still belong in the local ``.env`` and still load."""
    values = {}

    env_path = SCRIPT_DIR / ".env"
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


def quiet_sdk():
    warnings.filterwarnings("ignore")
    for name in ("google_genai", "google.genai", "google_genai.models"):
        logging.getLogger(name).setLevel(logging.ERROR)


def capture_source_dir():
    return Path(os.environ.get(
        "DREAD_CAPTURE_DIR", "/mnt/c/Users/steve/Videos/Captures"))


def slugify(s):
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower() or "capture"


def require_key():
    """Exit with the one instruction that fixes it, naming the vault file."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    path, _ = secrets_path()
    where = path or DEFAULT_SECRETS_PATH
    sys.exit(f"GEMINI_API_KEY not set: add the line to {where} (mode 0600), "
             f"or point {SECRETS_POINTER} at the vault file that holds it. "
             f"`dread.py env` shows what was found.")


def gen_config(resolution, **kw):
    """GenerateContentConfig with the media_resolution knob applied."""
    from google.genai import types
    if resolution and resolution != "default":
        kw["media_resolution"] = getattr(
            types.MediaResolution, f"MEDIA_RESOLUTION_{resolution.upper()}")
    return types.GenerateContentConfig(**kw)


def build_prompt(mode):
    return TRANSCRIBE_PROMPT.replace("{header}", PROMPT_HEADER[mode])


def upload_video(client, path):
    """Upload a local video to the Gemini Files API and wait until ACTIVE."""
    print(f"[uploading {path.name} "
          f"({path.stat().st_size / 1e6:.1f} MB)...]", file=sys.stderr)
    f = client.files.upload(file=str(path))
    while f.state.name == "PROCESSING":
        time.sleep(4)
        f = client.files.get(name=f.name)
    if f.state.name != "ACTIVE":
        sys.exit(f"Upload failed: file state {f.state.name}")
    print(f"[upload active: {f.name}]", file=sys.stderr)
    return f


def generate_with_retry(client, model, contents, config):
    from google.genai import errors
    chain = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_exc = None
    for m in chain:
        delay = BASE_DELAY_S
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return m, client.models.generate_content(
                    model=m, contents=contents, config=config)
            except errors.APIError as e:
                code = getattr(e, "code", None) or getattr(e, "status_code", None)
                if code in RETRYABLE:
                    last_exc = e
                    if attempt < MAX_ATTEMPTS:
                        print(f"[{m}: {code}; retry {attempt}/{MAX_ATTEMPTS - 1} "
                              f"in {delay}s]", file=sys.stderr)
                        time.sleep(delay)
                        delay *= 2
                else:
                    raise
        if m != chain[-1]:
            print(f"[{m}: exhausted retries; falling back]", file=sys.stderr)
    raise last_exc


def parse_json_reply(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"context": None, "messages": [],
                    "uncertainties": [], "raw_unparsed": text}


def transcribe(client, model, video_path, fps, mode, resolution):
    from google.genai import types
    gfile = upload_video(client, video_path)
    video_part = types.Part(
        file_data=types.FileData(file_uri=gfile.uri, mime_type=gfile.mime_type),
        video_metadata=types.VideoMetadata(fps=fps) if fps else None,
    )
    answered_model, resp = generate_with_retry(
        client, model,
        types.Content(parts=[video_part, types.Part(text=build_prompt(mode))]),
        gen_config(resolution, response_mime_type="application/json"),
    )
    try:
        client.files.delete(name=gfile.name)
    except Exception:
        pass  # files self-expire in 48h anyway
    return answered_model, resp


def render_markdown(payload, capture_id, label):
    lines = [f"# Transcript: {capture_id}", ""]
    if label:
        lines += [f"**Label:** {label}", ""]
    if payload.get("context"):
        lines += [f"**Context:** {payload['context']}", ""]
    cur_date = None
    for m in payload.get("messages", []):
        d = m.get("date")
        if d and d != cur_date:
            lines += [f"## {d}", ""]
            cur_date = d
        t = f" `{m['time']}`" if m.get("time") else ""
        reply = ""
        if m.get("reply_to"):
            quoted = m.get("reply_to_text")
            reply = (f" _(replying to {m['reply_to']}: \"{quoted}\")_" if quoted
                     else f" _(replying to {m['reply_to']})_")
        lines.append(f"**{m.get('author', '?')}**{t}{reply}")
        lines.append(m.get("text", ""))
        if m.get("attachments"):
            lines.append(f"> [attachment: {m['attachments']}]")
        lines.append("")
    unc = payload.get("uncertainties") or []
    if unc:
        lines += ["---", "## Uncertainties"]
        lines += [f"- {u}" for u in unc]
    return "\n".join(lines) + "\n"


def append_run_log(card, line):
    with open(card, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def cmd_ingest(args):
    from google import genai
    require_key()

    if args.file:
        src = Path(args.file)
        if not src.exists():
            sys.exit(f"No such file: {src}")
    else:
        cap_dir = capture_source_dir()
        vids = sorted(cap_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        if not vids:
            sys.exit(f"No .mp4 captures found in {cap_dir} "
                     "(is DREAD_CAPTURE_DIR right? did Game Bar save?)")
        src = vids[-1]
        age_min = (time.time() - src.stat().st_mtime) / 60
        if age_min > 30 and not args.yes:
            sys.exit(f"Newest capture is {age_min:.0f} min old ({src.name}). "
                     "If that's really the one, rerun with --yes, or pass --file.")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    capture_id = f"{ts}-{slugify(args.label)}" if args.label else ts
    dossier = CAPTURES_DIR / capture_id
    dossier.mkdir(parents=True, exist_ok=True)

    dest = dossier / f"source{src.suffix}"
    origin = str(src)
    if args.keep:
        shutil.copy2(src, dest)
    else:
        shutil.move(str(src), dest)

    card = dossier / "CARD.md"
    card.write_text(CARD_TEMPLATE.format(
        capture_id=capture_id, label=args.label or "(none)",
        date=datetime.now().strftime("%Y-%m-%d %H:%M"), mode=args.mode,
        source_name=dest.name, size_mb=dest.stat().st_size / 1e6,
        origin=origin))

    client = genai.Client()
    answered_model, resp = transcribe(client, args.model, dest,
                                      args.fps, args.mode, args.resolution)
    payload = parse_json_reply(resp.text)

    (dossier / "transcript.json").write_text(json.dumps(payload, indent=2))
    (dossier / "transcript.md").write_text(
        render_markdown(payload, capture_id, args.label))

    usage = getattr(resp, "usage_metadata", None)
    n_msgs = len(payload.get("messages", []))
    n_unc = len(payload.get("uncertainties") or [])
    append_run_log(card,
                   f"- {ts} ingest mode={args.mode} {answered_model} "
                   f"fps={args.fps} res={args.resolution} "
                   f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                   f"{getattr(usage, 'candidates_token_count', '?')}) — "
                   f"{n_msgs} messages, {n_unc} uncertainties")

    print(f"\n{n_msgs} messages transcribed ({n_unc} uncertainties)")
    print(f"transcript: {dossier / 'transcript.md'}")
    print(f"card:       {card}")
    if usage:
        print(f"[tokens: prompt={usage.prompt_token_count} "
              f"output={usage.candidates_token_count}]", file=sys.stderr)


def cmd_ask(args):
    from google import genai
    from google.genai import types
    require_key()

    dossier = CAPTURES_DIR / args.capture
    source = next(iter(dossier.glob("source.*")), None)
    if not source:
        sys.exit(f"No source video in {dossier} — is '{args.capture}' "
                 f"a capture id under {CAPTURES_DIR}?")
    card = dossier / "CARD.md"

    client = genai.Client()
    gfile = upload_video(client, source)
    prompt = (f"This video is a screen capture of a Discord channel advanced "
              f"page by page (brief hold on each page; consecutive pages "
              f"overlap slightly). Answer the question about its content. "
              f"Be specific; quote messages verbatim with author names where "
              f"relevant. QUESTION: {args.question}")
    video_part = types.Part(
        file_data=types.FileData(file_uri=gfile.uri, mime_type=gfile.mime_type),
        video_metadata=types.VideoMetadata(fps=args.fps) if args.fps else None,
    )
    answered_model, resp = generate_with_retry(
        client, args.model,
        types.Content(parts=[video_part, types.Part(text=prompt)]),
        gen_config(args.resolution),
    )
    try:
        client.files.delete(name=gfile.name)
    except Exception:
        pass

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = dossier / "runs" / ts
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "request.json").write_text(json.dumps({
        "capture": args.capture, "question": args.question,
        "model_requested": args.model, "model_answered": answered_model,
        "fps": args.fps, "resolution": args.resolution}, indent=2))
    (run_dir / "answer.md").write_text(resp.text)

    usage = getattr(resp, "usage_metadata", None)
    q_short = (args.question[:80] + "…") if len(args.question) > 80 else args.question
    append_run_log(card,
                   f"- {ts} ask {answered_model} res={args.resolution} "
                   f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                   f"{getattr(usage, 'candidates_token_count', '?')}) — "
                   f"Q: {q_short} — runs/{ts}/")

    print(resp.text)
    print(f"\n[archived to {run_dir}/]", file=sys.stderr)


def cmd_env(args):
    """Say where the credential came from and whether Google still accepts it.
    Never prints the value — length and a sha256 prefix are enough to tell two
    keys apart, which is the question this answers."""
    import urllib.error
    import urllib.request

    path, explicit = secrets_path()
    origin = f" (named by {SECRETS_POINTER})" if explicit else ""
    print(f"vault file : {path if path else '(none found)'}{origin}")
    local = SCRIPT_DIR / ".env"
    print(f"local .env : {local if local.exists() else '(none — correct)'}")

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        require_key()
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    print(f"credential : GEMINI_API_KEY, {len(key)} chars, sha256:{digest}")

    if args.no_check:
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


def main():
    load_env()
    quiet_sdk()

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("ingest", help="ingest a screen capture into a dossier")
    i.add_argument("--file", help="path to a capture video (default: newest "
                                  "mp4 in the Captures folder)")
    i.add_argument("--label", help="server/channel label, becomes part of "
                                   "the capture id")
    i.add_argument("--mode", choices=["page", "scroll"], default="page",
                   help="capture style: page (PgDn + ~1s holds, default) or "
                        "scroll (legacy fallback)")
    i.add_argument("--keep", action="store_true",
                   help="copy the source instead of moving it")
    i.add_argument("--yes", action="store_true",
                   help="accept a stale newest-capture without prompting")
    i.add_argument("--fps", type=float, default=DEFAULT_FPS,
                   help=f"sampling fps (default {DEFAULT_FPS})")
    i.add_argument("--resolution", choices=RESOLUTIONS,
                   default=DEFAULT_RESOLUTION,
                   help="Gemini media resolution (high, the default, reads "
                        "timestamps and reply headers; default/low is ~3.5x "
                        "cheaper and confabulates them)")
    i.add_argument("--model", default=DEFAULT_MODEL)
    i.set_defaults(func=cmd_ingest)

    a = sub.add_parser("ask", help="follow-up question against a capture")
    a.add_argument("--capture", required=True,
                   help="capture id (directory name under captures/)")
    a.add_argument("--question", required=True)
    a.add_argument("--fps", type=float, default=DEFAULT_FPS)
    a.add_argument("--resolution", choices=RESOLUTIONS,
                   default=DEFAULT_RESOLUTION)
    a.add_argument("--model", default=DEFAULT_MODEL)
    a.set_defaults(func=cmd_ask)

    v = sub.add_parser("env", help="where the credential came from, and does it work")
    v.add_argument("--no-check", action="store_true",
                   help="skip the live call to Google")
    v.set_defaults(func=cmd_env)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
