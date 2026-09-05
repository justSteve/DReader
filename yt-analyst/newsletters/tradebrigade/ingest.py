#!/usr/bin/env python3
"""Ingest Trade Brigade letters saved to disk by the Gmail connector. [dr-4ne]

The connector writes oversized get_thread results as JSON files under the
session's tool-results dir. This script turns each into
letters/<YYYY-MM-DD>_<threadId>.txt (plain text, small header) and keeps
letters/index.json. Identical bodies (Mailchimp resends) are recorded as
duplicates and not written twice.

    .venv/bin/python newsletters/tradebrigade/ingest.py [--src DIR ...]
"""
import argparse, glob, hashlib, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LETTERS = HERE / "letters"
INDEX = LETTERS / "index.json"
DEFAULT_SRC = glob.glob("/root/.claude/projects/-root-projects-DReader-yt-analyst/*/tool-results")

def body_of(m):
    return m.get("plaintextBody") or m.get("plaintext_body") or ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", nargs="*", default=DEFAULT_SRC)
    a = ap.parse_args()
    LETTERS.mkdir(parents=True, exist_ok=True)
    index = json.load(open(INDEX)) if INDEX.exists() else {}
    seen_hash = {v["sha1"]: k for k, v in index.items() if "sha1" in v}
    files = []
    for d in a.src:
        files += glob.glob(os.path.join(d, "mcp-claude_ai_Gmail-get_thread-*.txt"))
    new = dup = skip = 0
    for f in sorted(files):
        try:
            data = json.load(open(f))
        except Exception as e:
            print(f"unreadable {f}: {e}", file=sys.stderr); continue
        for m in data.get("messages", []):
            if "tradebrigade" not in (m.get("sender") or ""):
                continue
            tid = m.get("threadId") or data.get("id")
            if tid in index:
                skip += 1; continue
            body = body_of(m)
            if not body:
                print(f"no plaintext body in {f}", file=sys.stderr); continue
            h = hashlib.sha1(body.encode()).hexdigest()
            date = (m.get("date") or "")[:10]
            entry = {"date": date, "subject": m.get("subject", ""), "sha1": h,
                     "chars": len(body), "source": os.path.basename(f)}
            if h in seen_hash:
                entry["duplicate_of"] = seen_hash[h]; index[tid] = entry; dup += 1; continue
            # Mailchimp text has stray control chars in tracking URLs; keep the prose intact.
            body = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", body)
            out = LETTERS / f"{date}_{tid}.txt"
            out.write_text(f"# {entry['subject']}\n# sent: {m.get('date')}  thread: {tid}\n\n{body}")
            entry["file"] = out.name; index[tid] = entry; seen_hash[h] = tid; new += 1
    json.dump(dict(sorted(index.items(), key=lambda kv: kv[1]["date"], reverse=True)),
              open(INDEX, "w"), indent=1)
    uniq = sum(1 for v in index.values() if "file" in v)
    print(f"new={new} dup={dup} already={skip}  unique letters on disk={uniq}")

if __name__ == "__main__":
    main()
