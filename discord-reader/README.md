# discord-reader

Screen-captured page-throughs of Discord → Gemini → structured transcript.
Doctrine, invocation and verification live in CLAUDE.md; tool-level lessons
in LESSONS.md; per-capture dossiers under `captures/` (gitignored — private).

First trial ran 2026-09-12 (InvestiTrade #lessons, 5 messages, ~5 pages):
paged capture at 2 fps / 1 s holds lost nothing and produced no seam
duplicates. The one lever that mattered was Gemini's media resolution —
default (low) confabulated timestamps and dropped a message, high read them
all — so `--resolution high` is now the default. Details in LESSONS.md
("Verdicts — first ingest").

```
.venv/bin/python dread.py ingest --label "server/channel"
.venv/bin/python dread.py ask --capture <capture_id> --question "..."
.venv/bin/python dread.py env     # where the key came from; does it still work
```
