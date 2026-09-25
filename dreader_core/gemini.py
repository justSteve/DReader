"""Calling Gemini: which model, how to survive a busy one, how to read what it
says. yta.py's versions, which were the more hardened, are the ones kept;
dread.py inherits their fixes [dr-dqm.1]."""
import json
import logging
import re
import sys
import time
import warnings

DEFAULT_MODEL = "gemini-flash-latest"
# gemini-2.5-flash was retired 2026-09-06 and now 404s for new users,
# which turned a transient 503 into a hard traceback [dr-9qo].
FALLBACK_MODELS = ["gemini-3.6-flash"]
RETRYABLE = {429, 500, 503}
MAX_ATTEMPTS = 4
BASE_DELAY_S = 5


def quiet_sdk():
    warnings.filterwarnings("ignore")
    for name in ("google_genai", "google.genai", "google_genai.models"):
        logging.getLogger(name).setLevel(logging.ERROR)


def media_config(resolution, **kw):
    """GenerateContentConfig with the media_resolution knob applied. None and
    "default" leave the knob unset (yta passed None, dread passed "default")."""
    from google.genai import types
    if resolution and resolution != "default":
        kw["media_resolution"] = getattr(
            types.MediaResolution, f"MEDIA_RESOLUTION_{resolution.upper()}")
    return types.GenerateContentConfig(**kw)


def parse_json_reply(text, empty_diag=None, shape=None):
    """The reply as JSON; fences stripped if the model added them. When it is
    not JSON at all, return the caller's empty shape with the raw text kept."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            out = dict(shape or {})
            out.update({"uncertainties": [], "raw_unparsed": text,
                        "empty_response": empty_diag})
            return out


def response_text(resp, answered_model):
    """(text, empty_diag): surface why a reply is empty instead of dying in
    json.loads [dr-08s.9]."""
    text = resp.text
    if text is not None:
        return text, None
    cands = getattr(resp, "candidates", None) or []
    reasons = [str(getattr(c, "finish_reason", None)) for c in cands]
    fb = getattr(resp, "prompt_feedback", None)
    print(f"[empty response from {answered_model}: "
          f"finish_reasons={reasons} prompt_feedback={fb}]", file=sys.stderr)
    return "", {"finish_reasons": reasons, "prompt_feedback": str(fb) if fb else None}


def generate_with_retry(client, model, contents, config):
    """Call Gemini with backoff on transient errors, then model fallback.
    Returns (model_that_answered, response)."""
    from google.genai import errors
    import httpx

    chain = [model] + [m for m in FALLBACK_MODELS if m != model]
    last_exc = None
    for m in chain:
        delay = BASE_DELAY_S
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                resp = client.models.generate_content(
                    model=m, contents=contents, config=config
                )
                return m, resp
            except (errors.APIError, httpx.TransportError) as e:
                # httpx.TransportError covers "Server disconnected without
                # sending a response" (RemoteProtocolError), read timeouts
                # and connect errors — seen 2026-08-29 under parallel asks
                # [dr-8qq.13]; treat like a 503.
                code = (getattr(e, "code", None) or getattr(e, "status_code", None)
                        or (503 if isinstance(e, httpx.TransportError) else None))
                if code in RETRYABLE:
                    last_exc = e
                    if attempt < MAX_ATTEMPTS:
                        print(f"[{m}: {code}; retry {attempt}/{MAX_ATTEMPTS - 1} "
                              f"in {delay}s]", file=sys.stderr)
                        time.sleep(delay)
                        delay *= 2
                else:
                    # A non-retryable error on the PRIMARY model is the real
                    # answer — surface it (that is how API_KEY_INVALID reads).
                    # On a fallback it is noise, most often the model having
                    # been retired; keep the original 503 and move on.
                    if m == chain[0]:
                        raise
                    print(f"[{m}: {code}, not usable as a fallback]",
                          file=sys.stderr)
                    last_exc = last_exc or e
                    break
        if m != chain[-1]:
            print(f"[{m}: exhausted retries; falling back]", file=sys.stderr)
    raise last_exc
