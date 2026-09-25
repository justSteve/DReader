"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import subprocess


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
