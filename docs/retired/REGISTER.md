# Retirement register

What this repository has retired, and — the column that matters — **the premises
each retirement invalidates**. A ruling that lives only in a commit message is a
memory; a ruling with its invalidated premises written down is an invariant a
sweep can enforce (dr-n5v, check 5).

Read this before proposing anything that assumes one of the premises below. Code
for each retired track is preserved at the named git tag; findings are kept in
this directory.

## Retirements

### 2026-09-25 — the name yt-analyst  [dr-dqm]

Steve's ruling (2026-09-18, confirmed 09-25): *"the name YouTube-Analyst is too
YouTube specific … this repository manages media ingestion."* Renamed
`yt-analyst/` → `media-reader/`, `yta.py` → `mread.py`. `media-reader/yta.py` is a
forwarding shim that says so on stderr.

**Invalidates:**

- the path `yt-analyst/` in any command, doc or config (history files keep it)
- `yta.py` as the tool's name (the shim forwards; do not add features to it)
- `/root/.claude/projects/-root-projects-DReader-yt-analyst/` as where new
  session transcripts land (the newsletter ingester reads both)
- the premise that each collector keeps its own copy of credential, retry and
  upload code "by design" — `dreader_core/` holds the one copy, and
  `tests/test_tools_delegate.py` fails if a copy grows back

**Do not propose:** folding discord-reader into media-reader. Steve ruled 09-25
that it shares the core only.

### 2026-09-18 — the TypeScript query layer and the SQLite store  [dr-qyd]

Steve's ruling: *"we can safely cut all of it in that we are using a different
layer to produce the content."*

Removed: `src/` entire (Express API and its 7 routes, DatabaseService,
`schema.sql`, three CLI entries, ConfigLoader, the JSONL logger, ThreadAnalyzer,
28 tests), `package.json`, `tsconfig.json`, `jest.config.js`.
Code at tag **`query-layer-retired`**.

**Invalidates:**

- `data/dreader.db` as a serving store, and the `servers` / `channels` /
  `messages` / `scrape_jobs` schema in any form
- Discord API identity on a message: `id`, `author_id`, `message_url`,
  `embed_data`, `attachment_urls` — none of which the collector can supply
- the npm surface: `npm run dev`, `init-db`, `validate-config`, `db:reset`,
  `db:backup` (the last of which never existed — see residue)
- port 3001 as DReader's query address
- `discord-config.yaml` having any reader
- TypeScript as a language in this repository

**Do not propose:** rebuilding an Express/SQLite serving layer here. What siblings
can query, and how, is an enterprise convention (Steve, same day: *"every service
can expect to be queried by other services, and that has to be part of what being
a service is"*), and it sits behind the zentity definition — dr-ok8.

### 2026-09-12 — the Playwright retrieval track  [dr-4ov]

Browser automation of Steve's Discord account. Code at tag
**`playwright-retired`**; findings in this directory.

**Invalidates:** any solution assuming Discord API access, an account session,
cookies, headless operation, DOM selectors, scroll cadence, or machine-readable
message identity. Retrieval is Steve's screen captures transcribed by Gemini.

### 2026-04-28 — the TypeScript Playwright scrape-engine stack  [dr-4td]

The writer behind the query layer. Removed two years' assumptions ahead of its
reader, which is how the 2026-09-18 cut came to be necessary at all.

**Invalidates:** scrape jobs as a concept, incremental scroll-based collection,
and any claim that `dreader.db` is being written to. Last row written
2026-04-23 — five days before this retirement.

### 2026-07-23 — the `/checkpoint` auto-save loop  [co-59ywf]

Retired with the reason stated plainly in its own commit: *"write-only, nothing
reads it."* Listed here because it is the earliest recorded instance of the class
dr-n5v now names, and the phrase is the class's own definition.

## Residue — known, deliberate, not yet removed

Untracked files whose only reader has been retired. They are inert; they are
listed so nobody mistakes them for live configuration, and so the sweep can
count them.

| path | why it is residue | to remove |
|---|---|---|
| `discord-config.yaml` | `cookies_file`, `headless`, `scroll_delay_ms`, `max_scrolls` — parameters of a retrieval method retired 2026-09-12; its only reader was `validate-config`, removed 2026-09-18 | `rm discord-config.yaml` |
| `data/dreader.db` | 1 server, 1 channel, 3 scrape jobs, **0 messages**; nothing has written to it since 2026-04-23 | `rm data/dreader.db` |
| `data/chrome-profile/` | browser profile for the retired automation | `rm -rf data/chrome-profile` |
| `node_modules/`, `dist/`, `package-lock.json` | build output and dependencies of the removed npm project | `rm -rf node_modules dist package-lock.json` |

Left on disk rather than deleted because each is untracked, so removal is the one
step here that git cannot undo. Steve's call, one command each.

## Nothing was carried forward from the cut

`ThreadAnalyzer` was the only piece of the removed layer with any logic in it —
57 lines that walk `db.getReplies(id)` recursively and report depth and count. It
is bound to Discord message ids, which are on the invalidated list above, and the
algorithm is ordinary recursion. When transcript threads need rebuilding (forum
posts carry `reply_to` and `reply_to_text`), write it against the transcript's
own natural key rather than recovering this.
