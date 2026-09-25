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


def test_youtube_url_resolves_to_a_youtube_source():
    s = sources.resolve_source(ns(url="https://youtu.be/IUWvHVout94?t=3"))
    assert (s.kind, s.id, s.url, s.path) == (
        "youtube", "IUWvHVout94", "https://www.youtube.com/watch?v=IUWvHVout94", None)
    assert s.card.exists() and "**Kind:** youtube" in s.card.read_text()


def test_mp4_file_resolves_to_a_video_source(tmp_path):
    f = tmp_path / "rec.mp4"
    f.write_bytes(b"\0")
    s = sources.resolve_source(ns(file=str(f), id="it-orderflow-test"))
    assert (s.kind, s.id, s.path) == ("video", "it-orderflow-test", f.resolve())
    assert "**Kind:** video" in s.card.read_text()


def test_file_needs_an_id(tmp_path):
    f = tmp_path / "rec.mp4"
    f.write_bytes(b"\0")
    with pytest.raises(SystemExit, match="needs --id"):
        sources.resolve_source(ns(file=str(f)))


def test_unknown_extension_is_refused_naming_the_known_ones(tmp_path):
    f = tmp_path / "notes.xyz"
    f.write_bytes(b"\0")
    with pytest.raises(SystemExit, match=r"unsupported.*\.mp4"):
        sources.resolve_source(ns(file=str(f), id="some-notes"))


def test_existing_cards_are_never_rewritten(tmp_path):
    d = sources.DOSSIERS_DIR / "IUWvHVout94"
    d.mkdir(parents=True)
    (d / "CARD.md").write_text("# Video: IUWvHVout94\ncurated\n")
    s = sources.resolve_source(ns(url="https://www.youtube.com/watch?v=IUWvHVout94"))
    assert s.card.read_text() == "# Video: IUWvHVout94\ncurated\n"
