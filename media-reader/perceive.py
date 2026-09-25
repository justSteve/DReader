"""Asking Gemini: `ask` (one question, whole or clipped) and `transcribe` (local captures, chunked)."""

import sys
from pathlib import Path
_root = str(Path(__file__).resolve().parent.parent)  # dreader_core, after this dir
if _root not in sys.path:
    sys.path.insert(1, _root)
import json
import subprocess
from datetime import datetime

from dreader_core import creds, gemini, runs  # noqa: E402
from dreader_core.runs import parse_ts, fmt_ts  # noqa: E402
from prompts import TRANSCRIBE_PROMPT, ASK_SHAPE, ask_prompt  # noqa: E402
from sources import resolve_source, dossier_dir, media_part, probe_duration  # noqa: E402
import cuts  # noqa: E402


def window_label(start, end, crop):
    """The run-log line's bracketed window: a crop box, a clip range, or [full]."""
    if crop:
        return f" [crop {crop}]"
    if start or end:
        return f" [{start or '0:00'}-{end or 'end'}]"
    return " [full]"


def cmd_ask(args):
    from google import genai
    from google.genai import types

    src = resolve_source(args)
    # Flag guards come before the key check and the client: a bad flag
    # costs nothing and should say so first.
    if src.kind in ("document", "image") and (args.start or args.end or args.fps):
        sys.exit(f"ask: --start/--end/--fps do not apply to a {src.kind}; "
                 "ask about a page range in the question, or --crop an image")
    if src.kind == "audio":
        if args.fps:
            sys.exit("ask: audio has no frames; --fps does not apply")
        if args.start or args.end:
            sys.exit("ask: audio windows arrive in Task B4; "
                     "ask about the whole recording for now")
    cut, cut_mime, crop_box = None, None, None
    if getattr(args, "crop", None):
        if src.kind != "image":
            sys.exit("ask: --crop applies to images")
        crop_box = cuts.parse_box(args.crop)
        cut, cut_mime = cuts.crop(src.path, crop_box, dossier_dir(src.id) / "crops"), "image/png"
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
        "prompt_tokens": getattr(usage, "prompt_token_count", None),
        "output_tokens": getattr(usage, "candidates_token_count", None),
    }, indent=2))
    (run_dir / "response.json").write_text(json.dumps(payload, indent=2))

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

    creds.require_key("mread.py")
    if not getattr(args, "file", None):
        sys.exit("transcribe works on local captures: --file PATH --id ID")
    src = resolve_source(args)
    if src.kind != "video":
        sys.exit(f"transcribe: {src.kind} sources are not supported yet "
                 "(YouTube videos get captions from fetch_transcripts.py)")
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
