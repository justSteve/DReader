import httpx
import pytest
from google.genai import errors, types

from dreader_core import gemini


def api_error(code):
    return errors.APIError(code, {"error": {"message": f"http {code}", "status": "X"}})


class FakeModels:
    def __init__(self, script):
        self.script = {m: list(v) for m, v in script.items()}
        self.calls = []

    def generate_content(self, model, contents, config):
        self.calls.append(model)
        outcome = self.script[model].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FakeClient:
    def __init__(self, script):
        self.models = FakeModels(script)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(gemini.time, "sleep", lambda s: None)


def test_retries_a_503_then_answers():
    c = FakeClient({"m": [api_error(503), "ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("m", "ok")
    assert c.models.calls == ["m", "m"]


def test_falls_back_after_exhausting_the_primary(monkeypatch):
    monkeypatch.setattr(gemini, "FALLBACK_MODELS", ["fb"])
    c = FakeClient({"m": [api_error(503)] * gemini.MAX_ATTEMPTS, "fb": ["ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("fb", "ok")
    assert c.models.calls == ["m"] * gemini.MAX_ATTEMPTS + ["fb"]


def test_backoff_doubles_each_retry(monkeypatch):
    delays = []
    monkeypatch.setattr(gemini.time, "sleep", lambda s: delays.append(s))
    c = FakeClient({"m": [api_error(503)] * 3 + ["ok"]})
    gemini.generate_with_retry(c, "m", None, None)
    assert delays == [gemini.BASE_DELAY_S, 2 * gemini.BASE_DELAY_S, 4 * gemini.BASE_DELAY_S]


def test_non_retryable_on_the_primary_is_the_answer():
    c = FakeClient({"m": [api_error(400)]})
    with pytest.raises(errors.APIError) as e:
        gemini.generate_with_retry(c, "m", None, None)
    assert e.value.code == 400


def test_a_dead_fallback_is_skipped_and_the_original_error_kept(monkeypatch):
    monkeypatch.setattr(gemini, "FALLBACK_MODELS", ["retired"])
    c = FakeClient({"m": [api_error(503)] * gemini.MAX_ATTEMPTS,
                    "retired": [api_error(404)]})
    with pytest.raises(errors.APIError) as e:
        gemini.generate_with_retry(c, "m", None, None)
    assert e.value.code == 503


def test_transport_error_is_retried_like_a_503():
    c = FakeClient({"m": [httpx.RemoteProtocolError("Server disconnected"), "ok"]})
    assert gemini.generate_with_retry(c, "m", None, None) == ("m", "ok")


def test_no_retired_model_in_the_fallback_chain():
    # gemini-2.5-flash was retired 2026-09-06 [dr-9qo]; dread.py kept it until dr-dqm.
    assert "gemini-2.5-flash" not in gemini.FALLBACK_MODELS


def test_parse_plain_and_fenced_json():
    assert gemini.parse_json_reply('{"a": 1}') == {"a": 1}
    assert gemini.parse_json_reply('```json\n{"a": 1}\n```') == {"a": 1}


def test_parse_garbage_keeps_the_callers_shape():
    out = gemini.parse_json_reply("not json", shape={"summary": None, "claims": []})
    assert list(out) == ["summary", "claims", "uncertainties", "raw_unparsed", "empty_response"]
    assert out["raw_unparsed"] == "not json"


class Resp:
    text = None
    candidates = [type("C", (), {"finish_reason": "SAFETY"})()]
    prompt_feedback = None


def test_empty_reply_is_diagnosed_not_crashed():
    text, diag = gemini.response_text(Resp(), "m")
    assert text == "" and diag["finish_reasons"] == ["SAFETY"]


@pytest.mark.parametrize("res,expected", [
    (None, None), ("default", None),
    ("low", types.MediaResolution.MEDIA_RESOLUTION_LOW),
    ("high", types.MediaResolution.MEDIA_RESOLUTION_HIGH),
])
def test_media_config(res, expected):
    assert gemini.media_config(res).media_resolution == expected
