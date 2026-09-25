import json
import time
import types as pytypes

import pytest

from dreader_core import uploads


def fobj(name, state="ACTIVE"):
    return pytypes.SimpleNamespace(name=name, uri=f"uri/{name}", mime_type="video/mp4",
                                   state=pytypes.SimpleNamespace(name=state))


class FakeFiles:
    def __init__(self, states=("ACTIVE",)):
        self.uploads, self.configs, self._states = 0, [], list(states)

    def upload(self, file, config=None):
        self.uploads += 1
        self.configs.append(config)
        return fobj(f"files/{self.uploads}", self._states[0])

    def get(self, name):
        state = self._states.pop(0) if len(self._states) > 1 else self._states[0]
        return fobj(name, state)


class FakeClient:
    def __init__(self, **kw):
        self.files = FakeFiles(**kw)


def test_second_call_reuses_the_cached_handle(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 1


def test_a_changed_file_is_uploaded_again(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    src.write_bytes(b"x" * 11)
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 2


def test_waits_out_processing(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x")
    c = FakeClient(states=("PROCESSING", "PROCESSING", "ACTIVE"))
    assert uploads.upload_file(c, src).state.name == "ACTIVE"


def test_mime_type_is_passed_when_given(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.pdf"
    src.write_bytes(b"%PDF")
    c = FakeClient()
    uploads.upload_file(c, src, mime_type="application/pdf")
    assert c.files.configs == [{"mime_type": "application/pdf"}]


def test_no_mime_type_passes_none_config(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_file(c, src)
    assert c.files.configs == [None]


def test_expired_cache_entry_causes_reupload(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    cache = tmp_path / "upload.json"
    cache.write_text(json.dumps({
        "name": "files/stale", "uri": "uri/stale", "mime_type": "video/mp4",
        "path": str(src), "size": src.stat().st_size,
        "expires": time.time() - 100,
    }))
    c = FakeClient()
    uploads.upload_cached(c, cache, src)
    assert c.files.uploads == 1


def test_cached_handle_not_active_on_server_causes_reupload(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    c.files.get = lambda name: fobj(name, "FAILED")
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 2


def test_files_get_raising_causes_reupload(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src)

    def raise_get(name):
        raise RuntimeError("deleted server-side")
    c.files.get = raise_get
    uploads.upload_cached(c, tmp_path / "upload.json", src)
    assert c.files.uploads == 2


def test_cache_for_a_different_path_causes_reupload(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src_a = tmp_path / "a.mp4"
    src_a.write_bytes(b"x" * 10)
    src_b = tmp_path / "b.mp4"
    src_b.write_bytes(b"x" * 10)  # same size as a.mp4 — isolates path, not size
    c = FakeClient()
    uploads.upload_cached(c, tmp_path / "upload.json", src_a)
    uploads.upload_cached(c, tmp_path / "upload.json", src_b)
    assert c.files.uploads == 2


def test_corrupt_cache_json_causes_reupload(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    cache = tmp_path / "upload.json"
    cache.write_text("{not valid json")
    c = FakeClient()
    uploads.upload_cached(c, cache, src)
    assert c.files.uploads == 1


def test_upload_ending_failed_exits_and_writes_no_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.mp4"
    src.write_bytes(b"x" * 10)
    cache = tmp_path / "upload.json"
    c = FakeClient(states=("FAILED",))
    with pytest.raises(SystemExit):
        uploads.upload_cached(c, cache, src)
    assert not cache.exists()


def test_missing_server_mime_type_falls_back_to_caller_supplied(tmp_path, monkeypatch):
    monkeypatch.setattr(uploads.time, "sleep", lambda s: None)
    src = tmp_path / "a.pdf"
    src.write_bytes(b"%PDF")
    cache = tmp_path / "upload.json"
    c = FakeClient()
    c.files.upload = lambda file, config=None: pytypes.SimpleNamespace(
        name="files/1", uri="uri/1", mime_type=None,
        state=pytypes.SimpleNamespace(name="ACTIVE"))
    uploads.upload_cached(c, cache, src, mime_type="application/pdf")
    rec = json.loads(cache.read_text())
    assert rec["mime_type"] == "application/pdf"
