"""Documents: text extraction, and the quote check that is this kind's
independent verifier."""
import subprocess


def pdf_text(path):
    """pdftotext -layout; pages end in \\f. Empty string if poppler fails."""
    try:
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def page_count(path):
    if path.suffix.lower() != ".pdf":
        return 1
    return max(1, pdf_text(path).count("\f"))
