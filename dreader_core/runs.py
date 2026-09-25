"""Run archives: every Gemini call leaves runs/<timestamp>/ and one line in the
dossier card's run log."""
from datetime import datetime


def new_run_dir(dossier):
    """(ts, path) of a fresh dossier/runs/<ts>/. Parallel asks can share a
    second [dr-8qq.11]; never overwrite an archive."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = dossier / "runs" / ts
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        try:
            run_dir.mkdir()
            return ts, run_dir
        except FileExistsError:
            n += 1
            ts = f"{ts.split('-')[0]}-{ts.split('-')[1]}-{n}"
            run_dir = run_dir.parent / ts


def append_run_log(card, line):
    with open(card, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def parse_ts(s):
    """'HH:MM:SS' | 'MM:SS' | '95' -> seconds."""
    if s is None:
        return None
    sec = 0
    for p in str(s).split(":"):
        sec = sec * 60 + int(p)
    return sec


def fmt_ts(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"
