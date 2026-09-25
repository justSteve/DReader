import argparse
import json

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


def test_repointing_to_another_kind_is_refused(tmp_path):
    sources.resolve_source(ns(file=str(make(tmp_path, "a.pdf")), id="held-item"))
    with pytest.raises(SystemExit, match="refusing"):
        sources.resolve_source(ns(file=str(make(tmp_path, "b.png")), id="held-item"))


def test_repointing_within_a_kind_warns_and_updates(tmp_path, capsys):
    sources.resolve_source(ns(file=str(make(tmp_path, "a.pdf")), id="held-item"))
    b = make(tmp_path, "b.pdf")
    s = sources.resolve_source(ns(file=str(b), id="held-item"))
    assert "repointing" in capsys.readouterr().err
    rec = json.loads((s.card.parent / "source.json").read_text())
    assert rec["path"] == str(b.resolve())


def test_origin_survives_a_later_file_call(tmp_path):
    f = make(tmp_path, "ep.m4a")
    s = sources.resolve_source(ns(file=str(f), id="pod-ep-2",
                                  origin="https://example.com/ep2"))
    sources.resolve_source(ns(file=str(f), id="pod-ep-2"))
    rec = json.loads((s.card.parent / "source.json").read_text())
    assert rec["origin"] == "https://example.com/ep2"


def test_id_alone_with_a_moved_file_says_how_to_recover(tmp_path):
    f = make(tmp_path, "gone.png")
    sources.resolve_source(ns(file=str(f), id="moved-item"))
    f.unlink()
    with pytest.raises(SystemExit, match="which no longer exists"):
        sources.resolve_source(ns(id="moved-item"))


def test_id_alone_is_validated_before_any_path_is_built(tmp_path):
    # a source.json outside dossiers/ must not be reachable through ../
    outside = tmp_path / "x"
    outside.mkdir()
    (outside / "source.json").write_text(json.dumps(
        {"path": str(make(tmp_path, "o.png")), "origin": None}))
    with pytest.raises(SystemExit, match=r"--id \.\./x: not a dossier id"):
        sources.resolve_source(ns(id="../x"))


def test_plain_text_card_names_no_page_extent(tmp_path):
    s = sources.resolve_source(ns(file=str(make(tmp_path, "n.txt", b"hi")),
                                  id="note-item"))
    src_line = next(l for l in s.card.read_text().splitlines()
                    if l.startswith("- **Source:**"))
    assert "page" not in src_line


def test_unreadable_pdf_card_says_pages_unknown(tmp_path):
    s = sources.resolve_source(ns(file=str(make(tmp_path, "bad.pdf", b"not a pdf")),
                                  id="bad-pdf-item"))
    assert "pages unknown" in s.card.read_text()


# ------------------------------------------------------- corpus catch-up ----

def test_kind_tag_leaves_videos_untagged_and_names_other_kinds():
    import corpus
    assert corpus.kind_tag({"kind": "youtube"}) == ""
    assert corpus.kind_tag({"kind": "video"}) == ""
    assert corpus.kind_tag({}) == ""
    assert corpus.kind_tag({"kind": "document"}) == " · _document_"


@pytest.mark.parametrize("text,method", [
    ("verified by verify-quotes", "quote_check"),
    ("quote-checked against the letter", "quote_check"),
    ("see pages-3-4/ for the table", "page_image"),
    ("checked on the page image", "page_image"),
    ("crops/crop-10-20-300x40.png shows it", "crop"),
    ("a second pass over 1:00-1:40 agreed", "second_pass"),
    ("re-listened at 2:10", "second_pass"),
])
def test_export_reads_the_new_verification_words(text, method):
    import re
    import corpus
    pats = dict(corpus.VERIF_METHODS)
    assert re.search(pats[method], text, re.I)


def test_build_corpus_invents_a_youtube_url_only_for_youtube(tmp_path, monkeypatch):
    import build_corpus
    d = tmp_path / "dossiers"
    for vid, head in [("abcdefghijk", "- **URL:** https://www.youtube.com/watch?v=abcdefghijk"),
                      ("it-cap", "- **URL:** —"),
                      ("tb-letter", "- **Kind:** document")]:
        (d / vid).mkdir(parents=True)
        (d / vid / "CARD.md").write_text(f"# x\n\n{head}\n- **Status:** open\n\n## Findings\nok\n")
    monkeypatch.setattr(build_corpus, "VIDEOS", d)
    monkeypatch.setattr(build_corpus, "PLAYLISTS", tmp_path / "no-playlists")
    monkeypatch.setattr(build_corpus, "AUDIT", tmp_path / "no-AUDIT.md")
    cards = {c["id"]: c for c in build_corpus.build()["cards"]}
    assert (cards["abcdefghijk"]["kind"], cards["abcdefghijk"]["url"]) == (
        "youtube", "https://www.youtube.com/watch?v=abcdefghijk")
    assert (cards["it-cap"]["kind"], cards["it-cap"]["url"]) == ("video", "—")
    assert (cards["tb-letter"]["kind"], cards["tb-letter"]["url"]) == ("document", None)
