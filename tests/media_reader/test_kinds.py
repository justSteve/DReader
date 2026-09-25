import argparse

import pytest

import sources


@pytest.fixture(autouse=True)
def tmp_dossiers(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")


def ns(**kw):
    base = {"url": None, "file": None, "id": None}
    base.update(kw)
    return argparse.Namespace(**base)


def make(tmp_path, name, data=b"x"):
    f = tmp_path / name
    f.write_bytes(data)
    return f


@pytest.mark.parametrize("name,kind,mime", [
    ("a.pdf", "document", "application/pdf"),
    ("a.txt", "document", "text/plain"),
    ("a.md", "document", "text/markdown"),
    ("a.eml", "document", "message/rfc822"),
    ("a.html", "document", "text/html"),
    ("a.png", "image", "image/png"),
    ("a.JPG", "image", "image/jpeg"),
    ("a.webp", "image", "image/webp"),
    ("a.mp3", "audio", "audio/mpeg"),
    ("a.m4a", "audio", "audio/mp4"),
    ("a.wav", "audio", "audio/wav"),
    ("a.mp4", "video", "video/mp4"),
])
def test_kind_by_extension(tmp_path, name, kind, mime):
    s = sources.resolve_source(ns(file=str(make(tmp_path, name)), id="spec-item"))
    assert (s.kind, s.mime) == (kind, mime)


def test_non_video_kinds_get_the_media_card(tmp_path):
    s = sources.resolve_source(ns(file=str(make(tmp_path, "letter.txt", b"hello")),
                                  id="tb-letter-test"))
    text = s.card.read_text()
    assert text.startswith("# Media: tb-letter-test\n")
    assert "- **Kind:** document" in text and "letter.txt" in text
    assert "## Findings" in text and text.rstrip().endswith(
        "_(machine-appended by mread.py — do not edit above this line's entries)_")


def test_id_alone_finds_the_remembered_file(tmp_path):
    f = make(tmp_path, "chart.png")
    first = sources.resolve_source(ns(file=str(f), id="chart-one"))
    again = sources.resolve_source(ns(id="chart-one"))
    assert (again.kind, again.path, again.card) == (first.kind, first.path, first.card)


def test_id_alone_without_a_dossier_says_so():
    with pytest.raises(SystemExit, match="no remembered source"):
        sources.resolve_source(ns(id="never-seen"))


def test_origin_is_recorded_on_the_card(tmp_path):
    f = make(tmp_path, "ep.m4a")
    s = sources.resolve_source(ns(file=str(f), id="pod-ep-1",
                                  origin="https://example.com/ep1"))
    assert "https://example.com/ep1" in s.card.read_text()
