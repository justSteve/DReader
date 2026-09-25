"""Asking Gemini: `ask` (one question, whole or clipped) and `transcribe` (local captures, chunked)."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import json
import re
import subprocess
from datetime import datetime

from dreader_core import creds, gemini, runs  # noqa: E402
from dreader_core.runs import parse_ts, fmt_ts  # noqa: E402
from prompts import TRANSCRIBE_PROMPT, AUDIO_TRANSCRIBE_PROMPT, ASK_SHAPE, ask_prompt  # noqa: E402
from sources import resolve_source, dossier_dir, media_part, probe_duration  # noqa: E402
import sources  # noqa: E402
import cuts  # noqa: E402


def window_label(start, end, crop):
    """The run-log line's bracketed window: a crop box, a clip range, or [full]."""
    if crop:
        return f" [crop {crop}]"
    if start or end:
        return f" [{start or '0:00'}-{end or 'end'}]"
    return " [full]"


_CLIP_TS = re.compile(r"^\d+(?::\d+){0,2}$")


def clip_seconds(t):
    """Seconds for a clip-relative 'SS', 'MM:SS' or 'H:MM:SS' (or a whole
    number); None for anything else ("about 0:05", "1:10-1:20", 5.5)."""
    if isinstance(t, bool):
        return None
    if isinstance(t, int):
        return t if t >= 0 else None
    if isinstance(t, str) and _CLIP_TS.match(t.strip()):
        return parse_ts(t.strip())
    return None


def _note(payload, text):
    u = payload.get("uncertainties")
    if not isinstance(u, list):
        u = [u] if u else []
        payload["uncertainties"] = u
    u.append(text)


def rebase_items(payload, key, offset, missing_as_zero=False):
    """Shift payload[key][*]["t"] from clip time to file time, in place.
    Never raises: an item or t it cannot read stays as the model wrote it and
    is named in payload["uncertainties"]. The raw reply is archived first."""
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        return
    for c in payload[key]:
        if not isinstance(c, dict):
            _note(payload, f"{key[:-1]} {c!r} not re-based (not an object; offset {offset}s)")
            continue
        t = c.get("t")
        if t is None or t == "":
            if missing_as_zero:
                c["t"] = fmt_ts(offset)
            continue
        sec = clip_seconds(t)
        if sec is None:
            _note(payload, f"t {t!r} not re-based (clip-relative; offset {offset}s)")
        else:
            c["t"] = fmt_ts(sec + offset)


def rebase_claims(payload, offset):
    """A local cut starts at 0; the card speaks in file time."""
    rebase_items(payload, "claims", offset)


def _order(item):
    """Sort key for mixed re-based / un-rebasable items: unreadable last."""
    sec = clip_seconds(item.get("t")) if isinstance(item, dict) else None
    return (sec is None, sec or 0)


def audio_window(src, start, end, who):
    """(a, b) seconds for a local audio cut, clamped to the file's duration
    when ffprobe knows it."""
    total = probe_duration(src.path)
    a = parse_ts(start) if start else 0
    b = parse_ts(end) if end else total
    if total:
        if a >= total:
            sys.exit(f"{who}: --start {fmt_ts(a)} is at or past the end ({fmt_ts(total)})")
        b = min(b, total)
    elif not b:
        sys.exit(f"{who}: give an --end after --start (duration unknown)")
    return a, b, total


def cmd_ask(args):
    from google import genai
    from google.genai import types

    src = resolve_source(args)
    # Flag guards come before the key check and the client: a bad flag
    # costs nothing and should say so first.
    if src.kind in ("document", "image") and (args.start or args.end or args.fps):
        sys.exit(f"ask: --start/--end/--fps do not apply to a {src.kind}; "
                 "ask about a page range in the question, or --crop an image")
    if src.kind == "audio" and args.fps:
        sys.exit("ask: audio has no frames; --fps does not apply")
    cut, cut_mime, crop_box = None, None, None
    if getattr(args, "crop", None):
        if src.kind != "image":
            sys.exit("ask: --crop applies to images")
        crop_box = cuts.parse_box(args.crop)
        cut, cut_mime = cuts.crop(src.path, crop_box, dossier_dir(src.id) / "crops"), "image/png"
    # Audio windows are cut locally: VideoMetadata offsets apply to video only.
    offset = 0
    if src.kind == "audio" and (args.start or args.end):
        a, b, _ = audio_window(src, args.start, args.end, "ask")
        if b <= a:
            sys.exit("ask: give an --end after --start")
        cut, offset = cuts.cut_audio(src.path, a, b, dossier_dir(src.id) / "chunks"), a
    creds.require_key("mread.py")
    client = genai.Client()

    vm_kwargs = {}
    if src.kind in ("youtube", "video"):
        if args.start is not None:
            vm_kwargs["start_offset"] = f"{parse_ts(args.start)}s"
        if args.end is not None:
            vm_kwargs["end_offset"] = f"{parse_ts(args.end)}s"
        if args.fps is not None:
            vm_kwargs["fps"] = args.fps

    video_part = media_part(client, src, vm_kwargs, path=cut, mime=cut_mime)
    prompt = ask_prompt(src.kind, args.question)

    answered_model, resp = gemini.generate_with_retry(
        client,
        args.model,
        types.Content(parts=[video_part, types.Part(text=prompt)]),
        gemini.media_config(args.resolution, response_mime_type="application/json"),
    )

    text, empty_diag = gemini.response_text(resp, answered_model)
    payload = gemini.parse_json_reply(text, empty_diag, ASK_SHAPE)

    usage = getattr(resp, "usage_metadata", None)
    ts, run_dir = runs.new_run_dir(dossier_dir(src.id))
    (run_dir / "request.json").write_text(json.dumps({
        "kind": src.kind,
        "url": src.url, "file": str(src.path) if src.path else None,
        "question": args.question,
        "model_requested": args.model, "model_answered": answered_model,
        "start": args.start, "end": args.end, "fps": args.fps,
        "resolution": args.resolution,
        "crop": args.crop if crop_box else None,
        "offset_s": offset,
        "prompt_tokens": getattr(usage, "prompt_token_count", None),
        "output_tokens": getattr(usage, "candidates_token_count", None),
    }, indent=2))
    # The raw reply is paid for: archive it before anything can go wrong.
    (run_dir / "response.json").write_text(json.dumps(payload, indent=2))
    if offset:
        payload = json.loads(json.dumps(payload))
        rebase_claims(payload, offset)
        (run_dir / "response.rebased.json").write_text(json.dumps(payload, indent=2))

    window = window_label(args.start, args.end, args.crop if crop_box else None)
    q_short = (args.question[:80] + "…") if len(args.question) > 80 else args.question
    runs.append_run_log(src.card,
                   f"- {ts}{window} {answered_model} "
                   f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                   f"{getattr(usage, 'candidates_token_count', '?')}) — "
                   f"Q: {q_short} — runs/{ts}/")

    print(json.dumps(payload, indent=2))
    print(f"\n[model: {answered_model}] [card: {src.card}] "
          f"[archived to {run_dir}/]", file=sys.stderr)
    if usage:
        print(f"[tokens: prompt={usage.prompt_token_count} "
              f"output={usage.candidates_token_count}]", file=sys.stderr)


# ----------------------------------------------------------- transcribe ----
# The substrate for READ.md. YouTube videos get theirs free from yt-dlp
# (fetch_transcripts.py); a local capture has no caption track, so Gemini
# does it, in chunks so no single reply runs into the output limit.

def chunk_offset(payload, a, b, slack=15):
    """Offset to add to a chunk's timestamps so they are file-absolute.

    Returns 0 when the reply's timestamps already sit inside the window
    [a, b] (file frame) and a when they sit inside [0, b-a] (clip frame).
    A window starting at 0 is the same in both frames. When neither frame
    fits, prefer the clip frame the prompt asked for, and say so.
    """
    if a == 0:
        return 0
    ts = [parse_ts(x.get("t") or "0")
          for k in ("segments", "slides") for x in payload.get(k) or []]
    if not ts:
        return a
    lo, hi = min(ts), max(ts)
    if a - slack <= lo and hi <= b + slack:
        return 0
    if lo <= (b - a) + slack:
        return a
    print(f"[warn: chunk {fmt_ts(a)}-{fmt_ts(b)} timestamps span "
          f"{fmt_ts(lo)}-{fmt_ts(hi)}, fit neither frame; treating as clip-relative]",
          file=sys.stderr)
    return a


def cmd_transcribe(args):
    from google import genai
    from google.genai import types

    src = resolve_source(args)
    if src.kind == "audio":
        return transcribe_audio(args, src)
    if src.kind != "video":
        sys.exit(f"transcribe: {src.kind} sources are not supported "
                 "(YouTube videos get captions from fetch_transcripts.py)")
    creds.require_key("mread.py")
    vdir = dossier_dir(src.id)
    total = probe_duration(src.path)
    start = parse_ts(args.start) if args.start else 0
    end = parse_ts(args.end) if args.end else total
    if not end:
        sys.exit("could not determine the file's duration; give --end")
    chunk = int(args.chunk * 60)
    windows = [(a, min(a + chunk, end)) for a in range(start, end, chunk)]

    client = genai.Client()
    vm_base = {"fps": args.fps} if args.fps else {}
    # Named run_ids, not runs: the dreader_core.runs module import would
    # otherwise be shadowed for the rest of this function's scope.
    segments, slides, uncertainties, run_ids, tok_in, tok_out = [], [], [], [], 0, 0
    models = set()
    for a, b in windows:
        vm = dict(vm_base, start_offset=f"{a}s", end_offset=f"{b}s")
        print(f"[transcribe {fmt_ts(a)}-{fmt_ts(b)}]", file=sys.stderr)
        part = media_part(client, src, vm)
        answered, resp = gemini.generate_with_retry(
            client, args.model,
            types.Content(parts=[part, types.Part(text=TRANSCRIBE_PROMPT)]),
            gemini.media_config(args.resolution, response_mime_type="application/json"),
        )
        models.add(answered)
        text, empty_diag = gemini.response_text(resp, answered)
        payload = gemini.parse_json_reply(text, empty_diag, ASK_SHAPE)
        usage = getattr(resp, "usage_metadata", None)
        ts, run_dir = runs.new_run_dir(dossier_dir(src.id))
        (run_dir / "request.json").write_text(json.dumps({
            "file": str(src.path), "mode": "transcribe",
            "model_requested": args.model, "model_answered": answered,
            "start": fmt_ts(a), "end": fmt_ts(b), "fps": args.fps,
            "resolution": args.resolution,
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "output_tokens": getattr(usage, "candidates_token_count", None),
        }, indent=2))
        (run_dir / "response.json").write_text(json.dumps(payload, indent=2))
        run_ids.append(ts)
        tok_in += getattr(usage, "prompt_token_count", 0) or 0
        tok_out += getattr(usage, "candidates_token_count", 0) or 0

        # The window is a start/end offset on the WHOLE uploaded file, and
        # Gemini then timestamps from the file's start regardless of the
        # prompt rule (LESSONS.md 2026-09-17: it-orderflow-trapped-4304,
        # 10:00-13:15 chunk came back 10:00-13:04 and was re-based to 20:00+).
        # Detect which frame the reply is in and re-base only when needed;
        # --absolute forces the file frame.
        off = 0 if args.absolute else chunk_offset(payload, a, b)
        for seg in payload.get("segments") or []:
            seg["t"] = fmt_ts(parse_ts(seg.get("t") or "0") + off)
            segments.append(seg)
        for sl in payload.get("slides") or []:
            sl["t"] = fmt_ts(parse_ts(sl.get("t") or "0") + off)
            slides.append(sl)
        for u in payload.get("uncertainties") or []:
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] {u}")
        if payload.get("raw_unparsed"):
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] reply not JSON; "
                                 f"see runs/{ts}/response.json")
        runs.append_run_log(src.card,
                       f"- {ts} [{fmt_ts(a)}-{fmt_ts(b)}] {answered} "
                       f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                       f"{getattr(usage, 'candidates_token_count', '?')}) — "
                       f"transcribe — runs/{ts}/")

    segments.sort(key=lambda x: parse_ts(x["t"]))
    slides.sort(key=lambda x: parse_ts(x["t"]))
    out = {
        "id": src.id, "file": str(src.path), "duration_s": total,
        "window": [fmt_ts(start), fmt_ts(end)], "chunk_s": chunk,
        "models": sorted(models), "resolution": args.resolution or "default(low)",
        "fps": args.fps, "prompt_tokens": tok_in, "output_tokens": tok_out,
        "runs": run_ids, "segments": segments, "slides": slides,
        "uncertainties": uncertainties,
        "generated": datetime.now().isoformat(timespec="seconds"),
    }
    (vdir / "transcript.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    lines = [f"[{s['t']}] {(s.get('speech') or '').strip()}" for s in segments]
    (vdir / "transcript.txt").write_text("\n".join(lines) + "\n")
    md = [f"# Slides — {src.id}", "",
          f"_Transcribed by mread.py from `{src.path.name}`; every slide once, at first "
          "appearance, text verbatim as Gemini read it. Verify load-bearing numbers "
          "against frames._", ""]
    for sl in slides:
        md.append(f"## {sl['t']} — {sl.get('title') or '(untitled)'}")
        md.append("")
        for ln in (sl.get("text") or "").splitlines():
            if ln.strip():
                md.append(f"- {ln.strip()}")
        md.append("")
    if uncertainties:
        md.append("## Uncertainties")
        md.append("")
        md += [f"- {u}" for u in uncertainties]
        md.append("")
    (vdir / "slides.md").write_text("\n".join(md))

    thumb = vdir / "thumb.jpg"
    if not thumb.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(min(60, total // 2)),
                        "-i", str(src.path), "-frames:v", "1", "-vf", "scale=640:-1",
                        "-q:v", "6", str(thumb)], check=False)

    print(f"{src.id}: {len(segments)} segments, {len(slides)} slides, "
          f"{len(uncertainties)} uncertainties over {len(windows)} chunk(s); "
          f"tokens prompt={tok_in} output={tok_out}; models {sorted(models)}")
    print(f"[wrote {vdir / 'transcript.json'}, transcript.txt, slides.md]",
          file=sys.stderr)


def transcribe_audio(args, src):
    """Chunked speech transcript of an audio file: each window is cut locally,
    uploaded once (cached per chunk), and re-based onto file time."""
    from google import genai
    from google.genai import types

    creds.require_key("mread.py")
    d = dossier_dir(src.id)
    start, end, total = audio_window(src, args.start, args.end, "transcribe")
    chunk = int(args.chunk * 60)
    windows = [(a, min(a + chunk, end)) for a in range(start, end, chunk)]
    if not windows:
        sys.exit("transcribe: empty window (--start at or after --end)")
    client = genai.Client()
    # run_ids, not runs: runs is the dreader_core module.
    segments, uncertainties, run_ids, models, tok_in, tok_out = [], [], [], set(), 0, 0
    for a, b in windows:
        print(f"[transcribe {fmt_ts(a)}-{fmt_ts(b)}]", file=sys.stderr)
        piece = cuts.cut_audio(src.path, a, b, d / "chunks")
        part = media_part(client, src, path=piece)
        answered, resp = gemini.generate_with_retry(
            client, args.model,
            types.Content(parts=[part, types.Part(text=AUDIO_TRANSCRIBE_PROMPT)]),
            gemini.media_config(None, response_mime_type="application/json"))
        models.add(answered)
        text, diag = gemini.response_text(resp, answered)
        payload = gemini.parse_json_reply(text, diag, {"segments": []})
        usage = getattr(resp, "usage_metadata", None)
        ts, run_dir = runs.new_run_dir(d)
        (run_dir / "request.json").write_text(json.dumps({
            "kind": "audio", "file": str(src.path), "mode": "transcribe",
            "model_requested": args.model, "model_answered": answered,
            "start": fmt_ts(a), "end": fmt_ts(b), "offset_s": a,
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "output_tokens": getattr(usage, "candidates_token_count", None),
        }, indent=2))
        # Raw reply archived before re-basing: a paid reply is never lost.
        (run_dir / "response.json").write_text(json.dumps(payload, indent=2))
        run_ids.append(ts)
        tok_in += getattr(usage, "prompt_token_count", 0) or 0
        tok_out += getattr(usage, "candidates_token_count", 0) or 0
        if not isinstance(payload, dict):
            payload = {"segments": [], "uncertainties": [
                f"reply was not an object; see runs/{ts}/"]}
        rebase_items(payload, "segments", a, missing_as_zero=True)
        segments += [s for s in payload.get("segments") or [] if isinstance(s, dict)]
        u_list = payload.get("uncertainties")
        for u in (u_list if isinstance(u_list, list) else [u_list] if u_list else []):
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] {u}")
        if payload.get("raw_unparsed"):
            uncertainties.append(f"[{fmt_ts(a)}-{fmt_ts(b)}] reply not JSON; see runs/{ts}/")
        runs.append_run_log(src.card,
                            f"- {ts} [{fmt_ts(a)}-{fmt_ts(b)}] {answered} "
                            f"(tok {getattr(usage, 'prompt_token_count', '?')}/"
                            f"{getattr(usage, 'candidates_token_count', '?')}) — "
                            f"transcribe — runs/{ts}/")
    segments.sort(key=_order)
    (d / "transcript.json").write_text(json.dumps({
        "id": src.id, "kind": "audio", "file": str(src.path), "duration_s": total,
        "window": [fmt_ts(start), fmt_ts(end)], "chunk_s": chunk,
        "speaker_labels": "per chunk — Speaker N in one chunk is not "
                          "necessarily Speaker N in another",
        "models": sorted(models), "prompt_tokens": tok_in, "output_tokens": tok_out,
        "runs": run_ids, "segments": segments, "uncertainties": uncertainties,
        "generated": datetime.now().isoformat(timespec="seconds"),
    }, indent=2, ensure_ascii=False))
    (d / "transcript.txt").write_text("\n".join(
        f"[{s['t']}] {s.get('speaker') or '?'}: {(s.get('speech') or '').strip()}"
        for s in segments) + "\n")
    print(f"{src.id}: {len(segments)} segments, {len(uncertainties)} uncertainties over "
          f"{len(windows)} chunk(s); tokens prompt={tok_in} output={tok_out}")


# ---------------------------------------------------------------- fetch ----

def cmd_fetch(args):
    """Download a podcast episode (any page yt-dlp understands) as audio into
    the dossier, remember it, and create the card. Interrogate with --id after."""
    import argparse as _ap
    if not sources.LOCAL_ID_RE.match(args.id or ""):
        sys.exit("fetch needs --id: a slug naming dossiers/<id>/")
    d = dossier_dir(args.id)
    rec = d / "source.json"
    if rec.exists():
        old = json.loads(rec.read_text())
        old_kind = sources.KIND_BY_EXT.get(
            Path(old.get("path", "")).suffix.lower(), ("unknown",))[0]
        if old_kind != "audio":
            sys.exit(f"fetch: --id {args.id} already holds a {old_kind} "
                     f"({old.get('path')}); pick another --id")
        if old.get("origin") != args.url:
            for f in d.glob("source.*"):
                if f.name != "source.json":
                    f.unlink()
            print(f"[{args.id}: replacing audio from {old.get('origin')} with {args.url}]",
                  file=sys.stderr)
    ytdlp = Path(sys.executable).with_name("yt-dlp")
    ytdlp = str(ytdlp) if ytdlp.exists() else "yt-dlp"
    try:
        r = subprocess.run([ytdlp, "-x", "--audio-format", "m4a", "--force-overwrites",
                            "--print", "after_move:filepath",
                            "-o", str(d / "source.%(ext)s"), args.url],
                           check=True, capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit(f"fetch: yt-dlp not found ({ytdlp})")
    except subprocess.CalledProcessError as e:
        tail = "\n".join((e.stderr or "").strip().splitlines()[-5:])
        sys.exit(f"fetch: yt-dlp failed (exit {e.returncode}):\n{tail}")
    printed = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    got = Path(printed[-1]) if printed else None
    if not got or not got.is_file():
        sys.exit(f"fetch: yt-dlp reported no audio file in {d}/")
    src = resolve_source(_ap.Namespace(file=str(got), id=args.id, url=None,
                                       origin=args.url))
    print(f"{src.id}: {src.kind} {got.name} — card {src.card}")
