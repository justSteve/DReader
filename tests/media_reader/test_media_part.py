"""media_part's branches, with a recording stand-in for the upload cache:
no network, no client [dr-dqm.3]."""
from types import SimpleNamespace

import pytest

import sources
from sources import Source


@pytest.fixture
def uploads(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")
    calls = []

    def upload_cached(client, cache, path, mime):
        calls.append({"cache": cache, "path": path, "mime": mime})
        return SimpleNamespace(uri=f"https://files.example/{path.name}", mime_type=mime)

    monkeypatch.setattr(sources.uploads, "upload_cached", upload_cached)
    return calls


def local(tmp_path, name, kind, mime, data=b"x"):
    p = tmp_path / name
    p.write_bytes(data)
    return Source(kind=kind, id=f"t-{kind}", card=tmp_path / "CARD.md", path=p, mime=mime)


VM = {"start_offset": "10s", "end_offset": "20s"}


def test_youtube_is_a_file_uri_with_video_metadata_only_when_asked(uploads):
    src = Source(kind="youtube", id="abcdefghijk", card=None,
                 url="https://www.youtube.com/watch?v=abcdefghijk")
    part = sources.media_part(None, src, VM)
    assert part.file_data.file_uri == src.url
    assert part.video_metadata.start_offset == "10s"
    assert sources.media_part(None, src).video_metadata is None
    assert sources.media_part(None, src, {}).video_metadata is None
    assert uploads == []


def test_text_document_goes_inline_without_upload(tmp_path, uploads):
    src = local(tmp_path, "letter.txt", "document", "text/plain",
                b"SPY closed at 645.31. Watch 640 as support.\n")
    part = sources.media_part(None, src)
    assert "Watch 640 as support." in part.text
    assert part.file_data is None
    assert uploads == []


def test_pdf_goes_through_the_whole_file_upload_cache(tmp_path, uploads):
    src = local(tmp_path, "report.pdf", "document", "application/pdf")
    part = sources.media_part(None, src)
    assert uploads == [{"cache": sources.dossier_dir(src.id) / "upload.json",
                        "path": src.path, "mime": "application/pdf"}]
    assert part.file_data.file_uri == "https://files.example/report.pdf"
    assert part.file_data.mime_type == "application/pdf"
    assert part.video_metadata is None


def test_a_substituted_cut_gets_its_own_cache_beside_it(tmp_path, uploads):
    src = local(tmp_path, "talk.mp3", "audio", "audio/mpeg")
    cut = tmp_path / "chunk-0000-0600.mp3"
    cut.write_bytes(b"y")
    part = sources.media_part(None, src, path=cut)
    assert uploads[0]["cache"] == tmp_path / "chunk-0000-0600.mp3.upload.json"
    assert uploads[0]["path"] == cut and uploads[0]["mime"] == "audio/mpeg"
    assert part.file_data.file_uri == "https://files.example/chunk-0000-0600.mp3"


def test_video_keeps_video_metadata(tmp_path, uploads):
    src = local(tmp_path, "cap.mp4", "video", "video/mp4")
    part = sources.media_part(None, src, VM)
    assert part.video_metadata.end_offset == "20s"
    assert uploads[0]["cache"] == sources.dossier_dir(src.id) / "upload.json"


def test_audio_never_gets_video_metadata(tmp_path, uploads):
    src = local(tmp_path, "talk.mp3", "audio", "audio/mpeg")
    part = sources.media_part(None, src, VM)
    assert part.video_metadata is None
    assert part.file_data.mime_type == "audio/mpeg"
