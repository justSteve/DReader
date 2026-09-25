"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import email
import re
import subprocess
import unicodedata
from email import policy
from html.parser import HTMLParser


def pdf_text(path, layout=False):
    """pdftotext; pages end in \\f. Empty string if poppler fails.
    Default mode is reading order: quotes are checked against it, because
    -layout sets columns side by side and so splices sentences across them
    (the review's "Resistance at 640"). -layout is for human-read text.txt."""
    cmd = ["pdftotext", *(["-layout"] if layout else []), str(path), "-"]
    try:
        return subprocess.run(cmd,
                              capture_output=True, encoding="utf-8",
                              errors="replace", check=True, timeout=30).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError):
        return ""


def page_count(path):
    """Pages in a PDF, from pdfinfo; None if it cannot tell."""
    try:
        out = subprocess.run(["pdfinfo", str(path)], capture_output=True,
                             encoding="utf-8", errors="replace",
                             check=True, timeout=30).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError):
        return None
    for line in out.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1])
            except ValueError:
                return None
    return None


class _Text(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table"}
    CELL = {"td", "th"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            # A stray close tag must not leave the counter negative and so
            # swallow everything after it.
            self._skip = max(0, self._skip - 1)
        elif tag in self.BLOCK:
            self.out.append("\n")
        elif tag in self.CELL:
            self.out.append("\t")  # adjacent cells must not fuse: 640660

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)


def html_to_text(html):
    p = _Text()
    p.feed(html)
    return re.sub(r"\n{3,}", "\n\n", "".join(p.out)).strip() + "\n"


NO_TEXT_BODY = "[no text body]"


def email_text(path):
    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    head = "\n".join(f"{h}: {msg[h]}" for h in ("From", "To", "Date", "Subject") if msg[h])
    body = msg.get_body(preferencelist=("plain", "html"))
    if body is None:
        return f"{head}\n\n{NO_TEXT_BODY}"
    try:
        text = body.get_content()
    except (LookupError, UnicodeError):  # a charset Python does not know
        text = (body.get_payload(decode=True) or b"").decode("utf-8", "replace")
    if body.get_content_type() == "text/html":
        text = html_to_text(text)
    return f"{head}\n\n{text}"


def extract_text(path):
    """The document's text as Gemini's claims will be checked against it.
    PDFs in reading order (pages separated by \\f), never -layout."""
    suf = path.suffix.lower()
    if suf == ".pdf":
        return pdf_text(path, layout=False)
    if suf == ".eml":
        return email_text(path)
    if suf in (".html", ".htm"):
        return html_to_text(path.read_text(errors="replace"))
    return path.read_text(errors="replace")


# Typography a quote is forgiven, after NFKC has folded ligatures, the
# no-break space and the ellipsis. Escapes, so the table has no invisible
# characters.
_TYPO = str.maketrans({"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
                       "\u2014": "-", "\u2013": "-", "\u00a0": " ",
                       "\u2212": "-", "\u2010": "-", "\u2011": "-",
                       "\u00ad": "", "\u2026": "..."})


def normalise(s):
    """Forgive typography and whitespace; never digits, words or case."""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s.translate(_TYPO)).strip()


# A line-end hyphen (ASCII, U+2010 or soft) between two word characters.
# Joining the halves is only safe between LETTERS: "sup-\nport" is "support",
# but "5-\n10" is never "510". Keeping the hyphen is always safe.
_JOIN_LETTERS = re.compile(r"([^\W\d_])[-‐­]\n\s*([^\W\d_])")
_KEEP_HYPHEN = re.compile(r"(\w)[-‐­]\n\s*(\w)")


def _variants(text):
    """The text as a quote may legitimately match it, normalised: as
    extracted, with letter-letter line-end hyphens joined ("support"), and
    with the break dropped but the hyphen kept ("well-known", "640-660")."""
    return tuple(dict.fromkeys((
        normalise(text),
        normalise(_JOIN_LETTERS.sub(r"\1\2", text)),
        normalise(_KEEP_HYPHEN.sub(r"\1-\2", text)),
    )))


def _pattern(quote):
    """Anchored, so a quote cannot pass by stopping short of what the source
    says: "closed at 645" or "645." on "645.31", "640" on "6400", "12" on
    "12%", "12.5%" on "-12.5%" or "5%" on "0.5%"."""
    q = normalise(quote)
    if not q:
        return None
    pat = re.escape(q)
    if q[0].isdigit():
        pat = r"(?<![\w.,\-])" + pat   # no dropped sign, decimal or digits
    elif re.match(r"\w", q):
        pat = r"(?<!\w)" + pat
    if q[-1].isdigit():
        pat += r"(?![\w%]|[.,]\d)"     # no dropped digits, decimals or unit
    elif re.search(r"\w$", q):
        pat += r"(?![\w]|[.,]\d)"
    elif re.search(r"\d[.,]$", q):
        pat += r"(?!\d)"               # "645." is not the start of "645.31"
    return re.compile(pat)


def _found(pat, variants):
    return bool(pat) and any(pat.search(h) for h in variants)


def quote_found(quote, text):
    return _found(_pattern(str(quote)), _variants(text))


def check_quotes(claims, text):
    """[(claim, found)] for every claim that carries a verbatim quote."""
    v = _variants(text)
    return [(c, _found(_pattern(str(c["verbatim"])), v))
            for c in claims if c.get("verbatim")]


class PreparedText:
    """A document's text normalised once — whole, per page and per adjacent
    page pair (quotes that cross a break) — so checking N quotes does not
    normalise the document N times. Pages exist only when `paged` (a PDF,
    whose text is \f-separated)."""

    def __init__(self, text, paged):
        self.paged = paged
        self.whole = _variants(text)
        raw = text.split("\f") if paged else []
        self.pages = [_variants(p) for p in raw]
        self.pairs = [_variants(raw[i] + "\n" + raw[i + 1]) for i in range(len(raw) - 1)]


def locate_quote(quote, pages):
    """1-based numbers of the pages holding the quote. `pages` are raw page
    strings or PreparedText.pages."""
    pat = _pattern(str(quote))
    return [i for i, p in enumerate(pages, 1)
            if _found(pat, p if isinstance(p, tuple) else _variants(p))]


_PAGE_LABEL = re.compile(r"^\s*(?:p(?:age)?\.?\s*)?(\d+)\s*$", re.IGNORECASE)


def _page_no(page):
    """3, "3", "p. 3", "p.3", "page 3" -> 3; anything else -> None."""
    m = _PAGE_LABEL.match(str(page)) if page is not None else None
    return int(m[1]) if m else None


def quote_status(claim, text, paged):
    """"OK", "OK (page unchecked)", "MISSING" or "WRONG PAGE (found p.N)".
    `text` is the raw text or a PreparedText. Pages are checked only when
    paged and the claim names a page; a label that is not one page number
    ("3-4") is found-but-unchecked. A quote spanning a page break is OK on
    either page."""
    prep = text if isinstance(text, PreparedText) else PreparedText(text, paged)
    pat = _pattern(str(claim["verbatim"]))
    if not _found(pat, prep.whole):
        return "MISSING"
    label = claim.get("page")
    if not prep.paged or label is None or str(label).strip() == "":
        return "OK"
    page = _page_no(label)
    if page is None:
        return "OK (page unchecked)"
    hits = {i for i, p in enumerate(prep.pages, 1) if _found(pat, p)}
    for i, pair in enumerate(prep.pairs, 1):
        if not hits & {i, i + 1} and _found(pat, pair):
            hits |= {i, i + 1}
    if not hits:
        return "MISSING"
    if page in hits:
        return "OK"
    return f"WRONG PAGE (found p.{min(hits)})"
