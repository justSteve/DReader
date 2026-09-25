import documents

EML = b"""From: Matt <newsletter@tradebrigade.co>
To: steve@example.com
Date: Sun, 31 Aug 2026 18:02:00 -0400
Subject: Trade Brigade - Week Ahead
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="b"

--b
Content-Type: text/plain; charset="utf-8"

SPY closed at 645.31. Watch 640 as support.
--b
Content-Type: text/html; charset="utf-8"

<p>SPY closed at <b>645.31</b>.</p>
--b--
"""


def test_email_prefers_the_plain_part_and_keeps_headers(tmp_path):
    p = tmp_path / "l.eml"
    p.write_bytes(EML)
    t = documents.extract_text(p)
    assert "Subject: Trade Brigade - Week Ahead" in t
    assert "SPY closed at 645.31. Watch 640 as support." in t
    assert "<b>" not in t


def test_html_drops_tags_scripts_and_styles(tmp_path):
    p = tmp_path / "a.html"
    p.write_text("<style>x{}</style><h1>Title</h1><p>One &amp; two</p>"
                 "<script>alert(1)</script><p>three</p>")
    t = documents.extract_text(p)
    assert "Title" in t and "One & two" in t and "three" in t
    assert "alert" not in t and "x{}" not in t


def test_quote_normalisation_forgives_typography_not_digits():
    text = "He said “buy above 311” — then  waited."
    assert documents.quote_found('He said "buy above 311" - then waited.', text)
    assert not documents.quote_found('He said "buy above 312"', text)


def test_check_quotes_reports_each_claim():
    claims = [{"verbatim": "Watch 640 as support"}, {"verbatim": "Watch 650"},
              {"verbatim": None}, {"claim": "no verbatim key"}]
    rows = documents.check_quotes(claims, "SPY closed at 645.31. Watch 640 as support.")
    assert [r[1] for r in rows] == [True, False]


# --- quality-review fixes [dr-dqm.2] ------------------------------------------

import argparse  # noqa: E402
import json  # noqa: E402

import pytest  # noqa: E402

import sources  # noqa: E402


def make_pdf(pages):
    """A minimal Helvetica PDF: pages is a list of [(x, y, text)] runs.
    Hand-written because the venv has no PDF library; poppler reads it."""
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (
                " ".join(f"{4 + 2 * i} 0 R" for i in range(n)), n),
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    for i, runs in enumerate(pages):
        body = "".join(f"BT /F1 12 Tf {x} {y} Td ({t}) Tj ET\n" for x, y, t in runs)
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>")
        objs.append(f"<< /Length {len(body)} >>\nstream\n{body}endstream")
    out, offs = b"%PDF-1.4\n", []
    for k, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{k} 0 obj\n{o}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{o:010d} 00000 n \n" for o in offs).encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    return out


# Page 1 is two columns; side by side, -layout reads "Support at  Resistance at /
# 640 holds.  660 caps it." and so invents "Resistance at 640".
TWO_COL = [[(72, 700, "Support at"), (72, 685, "640 holds."), (72, 670, "Buyers defend it."),
            (340, 700, "Resistance at"), (340, 685, "660 caps it."),
            (340, 670, "Sellers wait there.")],
           [(72, 700, "Target 700 by Friday.")]]


@pytest.fixture
def two_col_pdf(tmp_path):
    p = tmp_path / "two-col.pdf"
    p.write_bytes(make_pdf(TWO_COL))
    return p


# 1. anchored matching
@pytest.mark.parametrize("quote,found", [
    ("SPY closed at 645", False), ("Stop at 640", False), ("Revenue fell 1", False),
    ("SPY closed at 645.31", True), ("Stop at 6400", True), ("Revenue fell 12%", True),
    ("closed at 645.31.", True),
])
def test_quotes_are_anchored_at_number_and_word_edges(quote, found):
    text = "SPY closed at 645.31. Stop at 6400. Revenue fell 12%."
    assert documents.quote_found(quote, text) is found


def test_blank_quote_is_never_found():
    assert not documents.quote_found("   ", "anything")


# 2. reading-order text for PDFs
def test_pdf_quotes_check_against_reading_order_not_layout(two_col_pdf):
    layout = documents.pdf_text(two_col_pdf, layout=True)
    assert documents.quote_found("Resistance at 640", layout)  # the trap is real
    text = documents.extract_text(two_col_pdf)
    assert not documents.quote_found("Resistance at 640", text)
    assert documents.quote_found("Support at 640 holds.", text)
    assert documents.quote_found("Resistance at 660 caps it.", text)


# 3. hyphenated line breaks
def test_hyphenated_line_breaks_are_joined_both_ways():
    assert documents.quote_found("We continue to support the rally.",
                                 "We continue to sup-\nport the rally.")
    assert documents.quote_found("a well-known level", "a well-\nknown level")


# 4. unicode
def test_normalise_forgives_minus_ligatures_ellipsis_and_soft_hyphens():
    assert documents.quote_found("fell -2.5%", "fell −2.5%")
    assert documents.quote_found("an efficient market", "an eﬃcient market")
    assert documents.quote_found("wait...", "wait…")
    assert documents.quote_found("support", "sup­port")
    assert documents.quote_found("non-farm", "non‑farm")


# 5, 6. HTML
def test_html_table_cells_stay_separate():
    t = documents.html_to_text("<table><tr><td>640</td><td>660</td></tr></table>")
    assert documents.quote_found("640", t) and documents.quote_found("660", t)
    assert "640660" not in t


def test_stray_close_tag_does_not_swallow_later_text():
    t = documents.html_to_text("<p>one</p></style><p>two</p><style>x{}</style><p>three</p>")
    assert "two" in t and "three" in t and "x{}" not in t


# 7. email
NO_BODY = b"""From: a@b.c
Subject: Chart only
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="b"

--b
Content-Type: image/png
Content-Transfer-Encoding: base64

iVBORw0KGgo=
--b--
"""

BOGUS_CHARSET = b"""From: a@b.c
Subject: Odd charset
Content-Type: text/plain; charset="x-no-such-charset"

Watch 640 as support.
"""


def test_email_without_a_text_body_says_so(tmp_path):
    p = tmp_path / "n.eml"
    p.write_bytes(NO_BODY)
    t = documents.extract_text(p)
    assert "Subject: Chart only" in t and t.endswith("[no text body]")


def test_email_with_unknown_charset_falls_back_to_utf8(tmp_path):
    p = tmp_path / "c.eml"
    p.write_bytes(BOGUS_CHARSET)
    assert "Watch 640 as support." in documents.extract_text(p)


# 9. page check
def test_locate_quote_and_page_status(two_col_pdf):
    text = documents.extract_text(two_col_pdf)
    pages = text.split("\f")
    assert documents.locate_quote("Target 700 by Friday.", pages) == [2]
    st = lambda page, q: documents.quote_status({"page": page, "verbatim": q}, text, paged=True)  # noqa: E731
    assert st(2, "Target 700 by Friday.") == "OK"
    assert st("2", "Target 700 by Friday.") == "OK"
    assert st(1, "Target 700 by Friday.") == "WRONG PAGE (found p.2)"
    assert st(1, "Target 800") == "MISSING"
    assert st(None, "Target 700 by Friday.") == "OK"
    assert documents.quote_status({"page": 1, "verbatim": "Target 700"}, text,
                                  paged=False) == "OK"


def test_quote_spanning_a_page_break_is_ok_on_either_page():
    pages = ["intro. Buyers step in", "at 640 and hold.", ""]
    text = "\f".join(pages)
    for page in (1, 2):
        assert documents.quote_status({"page": page, "verbatim": "step in at 640"},
                                      text, paged=True) == "OK"
    assert documents.quote_status({"page": 3, "verbatim": "step in at 640"},
                                  text, paged=True).startswith("WRONG PAGE")


# 8. verify-quotes robustness (and 7's refusal)
@pytest.fixture
def dossiers(tmp_path, monkeypatch):
    monkeypatch.setattr(sources, "DOSSIERS_DIR", tmp_path / "dossiers")
    return tmp_path / "dossiers"


def ns(**kw):
    base = {"url": None, "file": None, "id": None, "run": None}
    base.update(kw)
    return argparse.Namespace(**base)


def write_run(dossiers, did, name, claims):
    d = dossiers / did / "runs" / name
    d.mkdir(parents=True)
    (d / "response.json").write_text(json.dumps({"claims": claims}))


def test_numeric_verbatim_is_checked_not_crashed(tmp_path, dossiers, capsys):
    import verify
    doc = tmp_path / "l.txt"
    doc.write_text("SPY closed at 645.31. Stop at 6400.\n")
    args = ns(file=str(doc), id="num-quote")
    sources.resolve_source(args)
    write_run(dossiers, "num-quote", "20260925-120000", [{"page": None, "verbatim": 645.31}])
    (dossiers / "num-quote" / "runs" / "odd-name").mkdir()  # tolerated by the sort
    with pytest.raises(SystemExit) as e:
        verify.cmd_verify_quotes(args)
    assert e.value.code == 0
    assert "645.31" in capsys.readouterr().out


def test_wrong_page_fails_the_exit_code(two_col_pdf, dossiers, capsys):
    import verify
    args = ns(file=str(two_col_pdf), id="two-col")
    sources.resolve_source(args)
    write_run(dossiers, "two-col", "20260925-120000",
              [{"page": 1, "verbatim": "Support at 640 holds."},
               {"page": 1, "verbatim": "Target 700 by Friday."}])
    with pytest.raises(SystemExit) as e:
        verify.cmd_verify_quotes(args)
    out = capsys.readouterr().out
    assert e.value.code == 1
    assert "WRONG PAGE (found p.2)" in out


def test_missing_run_and_missing_runs_dir_exit_cleanly(tmp_path, dossiers):
    import verify
    doc = tmp_path / "l.txt"
    doc.write_text("text\n")
    args = ns(file=str(doc), id="no-runs")
    sources.resolve_source(args)
    with pytest.raises(SystemExit) as e:
        verify.cmd_verify_quotes(args)
    assert "no runs" in str(e.value.code)
    write_run(dossiers, "no-runs", "20260925-120000", [])
    args.run = "20260101-000000"
    with pytest.raises(SystemExit) as e:
        verify.cmd_verify_quotes(args)
    assert "no run 20260101-000000" in str(e.value.code)


def test_verify_quotes_refuses_an_email_with_no_text_body(tmp_path, dossiers):
    import verify
    p = tmp_path / "n.eml"
    p.write_bytes(NO_BODY)
    args = ns(file=str(p), id="no-body")
    sources.resolve_source(args)
    write_run(dossiers, "no-body", "20260925-120000", [{"verbatim": "Chart only"}])
    with pytest.raises(SystemExit) as e:
        verify.cmd_verify_quotes(args)
    assert "no text body in n.eml" in str(e.value.code)


# 10. ask guards fire before any client or key
@pytest.mark.parametrize("flags,msg", [
    ({"fps": 2.0}, "audio has no frames"),
    ({"start": "01:00"}, "audio windows arrive in Task B4"),
    ({"end": "02:00"}, "audio windows arrive in Task B4"),
])
def test_ask_rejects_windows_and_fps_for_audio(tmp_path, dossiers, monkeypatch, flags, msg):
    import perceive
    from google import genai

    def boom(*a, **k):
        raise AssertionError("guard must fire before this")
    monkeypatch.setattr(perceive.creds, "require_key", boom)
    monkeypatch.setattr(genai, "Client", boom)
    mp3 = tmp_path / "talk.mp3"
    mp3.write_bytes(b"x")
    base = {"start": None, "end": None, "fps": None, "question": "q",
            "resolution": None, "model": "m"}
    base.update(flags)
    with pytest.raises(SystemExit) as e:
        perceive.cmd_ask(ns(file=str(mp3), id="talk-guard", **base))
    assert msg in str(e.value.code)


# 11. pages validates its range before touching disk
@pytest.mark.parametrize("first,last,msg", [
    (2, 1, "--first 2 is after --last 1"), (0, 1, "pages start at 1"),
    (1, 5, "has 2 page(s)"),
])
def test_pages_rejects_a_bad_range(two_col_pdf, dossiers, first, last, msg):
    import verify
    args = ns(file=str(two_col_pdf), id="two-col-pages", first=first, last=last, dpi=50)
    with pytest.raises(SystemExit) as e:
        verify.cmd_pages(args)
    assert msg in str(e.value.code)
    assert not list((dossiers / "two-col-pages").glob("pages-*"))


def test_pages_renders_images_and_layout_text(two_col_pdf, dossiers):
    import verify
    verify.cmd_pages(ns(file=str(two_col_pdf), id="two-col-pages", first=1, last=2, dpi=50))
    out = dossiers / "two-col-pages" / "pages-1-2"
    assert len(list(out.glob("p-*.png"))) == 2
    assert "Support at          Resistance at" in (out / "text.txt").read_text()


# --- re-review fixes [dr-dqm.2] -----------------------------------------------

# 1. a trailing period after a digit is not the end of the number
def test_trailing_period_after_a_digit_does_not_end_the_number():
    assert not documents.quote_found("SPY closed at 645.", "SPY closed at 645.31.")
    assert documents.quote_found("SPY closed at 645.", "SPY closed at 645. Then")


# 2. hyphenated line breaks join letters only
def test_hyphen_join_is_letters_only():
    assert not documents.quote_found("buy 510 contracts", "buy 5-\n10 contracts")
    assert not documents.quote_found("640660", "zone 640-\n660")
    assert documents.quote_found("640-660", "zone 640-\n660")
    assert documents.quote_found("support", "sup-\nport")


# 3. a dropped sign or decimal point is a different number
def test_a_dropped_leading_sign_fails():
    assert not documents.quote_found("12.5%", "loss of −12.5% today")
    assert not documents.quote_found("12.5%", "loss of -12.5% today")
    assert not documents.quote_found("5%", "yield 0.5% today")
    assert documents.quote_found("12.5%", "gain of 12.5% today")
    assert documents.quote_found("645", "SPY at $645 today")
    assert documents.quote_found("$645", "SPY at $645 today")


# 4. a dropped unit is a different claim
def test_a_dropped_percent_fails():
    assert not documents.quote_found("up 12", "up 12% on the week")
    assert documents.quote_found("up 12%", "up 12% on the week")


# 5. page labels
@pytest.mark.parametrize("label", ["p. 2", "p.2", "page 2", "Page 2", 2, "2"])
def test_page_labels_parse_to_a_number(label):
    text = "one\fTarget 700 by Friday.\f"
    assert documents.quote_status({"page": label, "verbatim": "Target 700"},
                                  text, paged=True) == "OK"
    assert documents.quote_status({"page": label, "verbatim": "one"},
                                  text, paged=True) == "WRONG PAGE (found p.1)"


def test_unparseable_page_label_is_found_but_unchecked():
    text = "one\fTarget 700 by Friday.\f"
    assert documents.quote_status({"page": "3-4", "verbatim": "Target 700"},
                                  text, paged=True) == "OK (page unchecked)"
    assert documents.quote_status({"page": "3-4", "verbatim": "Target 800"},
                                  text, paged=True) == "MISSING"


# 6. prepared once, same answers
def test_prepared_text_gives_the_same_statuses():
    text = "intro. Buyers step in\fat 640 and hold.\fTarget 700.\f"
    prep = documents.PreparedText(text, paged=True)
    for page, q in [(1, "step in at 640"), (3, "Target 700."), (1, "Target 700."),
                    (2, "Target 800"), ("2-3", "and hold.")]:
        c = {"page": page, "verbatim": q}
        assert documents.quote_status(c, prep, paged=True) == \
            documents.quote_status(c, text, paged=True)
    assert documents.locate_quote("Target 700.", prep.pages) == [3]
