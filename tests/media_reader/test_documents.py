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
