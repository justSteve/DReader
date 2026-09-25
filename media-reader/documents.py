"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import email
import re
import subprocess
from email import policy
from html.parser import HTMLParser


def pdf_text(path):
    """pdftotext -layout; pages end in \\f. Empty string if poppler fails."""
    try:
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
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
            self._skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)


def html_to_text(html):
    p = _Text()
    p.feed(html)
    return re.sub(r"\n{3,}", "\n\n", "".join(p.out)).strip() + "\n"


def email_text(path):
    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    head = "\n".join(f"{h}: {msg[h]}" for h in ("From", "To", "Date", "Subject") if msg[h])
    body = msg.get_body(preferencelist=("plain", "html"))
    text = body.get_content() if body else ""
    if body is not None and body.get_content_type() == "text/html":
        text = html_to_text(text)
    return f"{head}\n\n{text}"


def extract_text(path):
    """The document's text as Gemini's claims will be checked against it."""
    suf = path.suffix.lower()
    if suf == ".pdf":
        return pdf_text(path)
    if suf == ".eml":
        return email_text(path)
    if suf in (".html", ".htm"):
        return html_to_text(path.read_text(errors="replace"))
    return path.read_text(errors="replace")


# Curly quotes, em/en dashes and the no-break space, written as escapes so
# the table has no invisible characters.
_TYPO = str.maketrans({"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
                       "\u2014": "-", "\u2013": "-", "\u00a0": " "})


def normalise(s):
    """Forgive typography and whitespace; never digits, words or case."""
    return re.sub(r"\s+", " ", s.translate(_TYPO)).strip()


def quote_found(quote, text):
    return normalise(quote) in normalise(text)


def check_quotes(claims, text):
    """[(claim, found)] for every claim that carries a verbatim quote."""
    return [(c, quote_found(c["verbatim"], text))
            for c in claims if c.get("verbatim")]
