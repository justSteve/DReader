"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import email
import re
import subprocess
import unicodedata
from functools import lru_cache
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


_LINE_HYPHEN = re.compile(r"(\w)[-\u2010\u00ad]\n\s*(\w)")


@lru_cache(maxsize=32)
def _haystacks(text):
    """The text as a quote may legitimately match it: as extracted, with
    hyphenated line breaks joined ("sup-\\nport" -> "support"), and with the
    break dropped but the hyphen kept ("well-\\nknown" -> "well-known")."""
    return tuple(dict.fromkeys((
        normalise(text),
        normalise(_LINE_HYPHEN.sub(r"\1\2", text)),
        normalise(_LINE_HYPHEN.sub(r"\1-\2", text)),
    )))


def _pattern(quote):
    """Anchored: a quote must not end inside a longer number or word, so
    "closed at 645" does not pass on "closed at 645.31", nor "640" on "6400"."""
    q = normalise(quote)
    if not q:
        return None
    pat = re.escape(q)
    if re.match(r"\w", q):
        pat = r"(?<!\w)" + pat
    if re.search(r"\w$", q):
        pat += r"(?![\w]|[.,]\d)"
    return re.compile(pat)


def quote_found(quote, text):
    pat = _pattern(str(quote))
    return bool(pat) and any(pat.search(h) for h in _haystacks(text))


def check_quotes(claims, text):
    """[(claim, found)] for every claim that carries a verbatim quote."""
    return [(c, quote_found(str(c["verbatim"]), text))
            for c in claims if c.get("verbatim")]


def locate_quote(quote, pages):
    """1-based numbers of the pages whose text holds the quote."""
    return [i for i, p in enumerate(pages, 1) if quote_found(quote, p)]


def _page_no(page):
    try:
        return int(str(page).strip())
    except (TypeError, ValueError):
        return None


def quote_status(claim, text, paged):
    """"OK", "MISSING" or "WRONG PAGE (found p.N)". Pages are checked only
    when `paged` (a PDF, whose text is \\f-separated) and the claim names a
    numeric page; a quote spanning a page break is OK on either page."""
    q = str(claim["verbatim"])
    page = _page_no(claim.get("page")) if paged else None
    if page is None:
        return "OK" if quote_found(q, text) else "MISSING"
    pages = text.split("\f")
    hits = set(locate_quote(q, pages))
    for i in range(len(pages) - 1):
        if quote_found(q, pages[i] + "\n" + pages[i + 1]) and not hits & {i + 1, i + 2}:
            hits |= {i + 1, i + 2}
    if not hits:
        return "MISSING"
    if page in hits:
        return "OK"
    return f"WRONG PAGE (found p.{min(hits)})"
