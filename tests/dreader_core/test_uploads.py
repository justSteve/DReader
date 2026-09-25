import types as pytypes

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
