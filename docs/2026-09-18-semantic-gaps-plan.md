# Semantic gaps: built, but never demonstrated

Steve, 2026-09-18: *"this is the general shape of an error that our code
frequently makes: build something to do something then don't test and validate
the output."* This is that shape named, measured in one repository, and the plan
to make existing code surface it and future code refuse it.

## 1. The gap, defined so it can be detected

A **semantic gap** is the distance between what an artifact *declares* and what
any execution has ever *demonstrated*.

It is not a bug. Every specimen below is syntactically correct, most compile,
several pass their tests. It is a claim nobody has cashed. Formally: something
declares a capability, and no run exists whose output was compared against an
independent source.

Three properties make it invisible:

- Declaring costs nothing — a line in `package.json`, a column in a schema, a
  row in an architecture table.
- The usual gates check **internal consistency**, never **correspondence**. A
  compiler checks types against types. A test checks code against a fixture the
  test itself wrote.
- Documentation repeats the declaration, and repetition reads as corroboration.

The diagnostic question is not *"is there a test?"* It is:

> **Has this thing's output ever been compared to the world it claims to describe?**

## 2. Specimens — one repository, one sweep, 2026-09-18

| # | The declaration | What is demonstrated | Form |
|---|---|---|---|
| 1 | `npm run db:backup`, declared in `package.json` and in CLAUDE.md's architecture table | `src/cli/db-backup.ts` **does not exist**; the command has never been run | declared, absent |
| 2 | `npm run validate-config` — passes, reports "Cookies file: data/cookies.json", 4 servers, 16 channels | `data/cookies.json` does not exist; `headless`, `scroll_delay_ms`, `max_scrolls` are parameters of the retrieval method **retired 2026-09-12** (dr-4ov) | validator that checks shape, never correspondence |
| 3 | `messages` table, the serving half of the query API | **0 rows**; last write 2026-04-23, five days before its writer was retired (dr-4td, 2026-04-28) | producer retired, consumer left standing |
| 4 | 7 API routes across 4 route files | 2 covered by a test, **0 consumers** in any sibling repo | orphan surface |
| 5 | 13 of 28 tests (DatabaseService, ConfigLoader) | assert against the retired scrape schema using inline literals; **no suite reads a file any collector produced** | tests pinning a dead contract |
| 6 | 4 of 28 tests (`types.test.ts`) | construct an object, assert the fields just assigned; no symbol under test is called | tautological test |
| 7 | dr-5f2 — "map transcript.json messages onto schema.sql" | the schema requires `id`, `author_id`, `message_url NOT NULL`; the transcript has none of them. The mapping was specified without once running real transcript data at the schema | spec written without contact with its input |
| 8 | The 2026-08-24 fact sheet — built, rendered, read by two narrators, graded | its overnight range was never compared to the tape. Wrong by 16.75 points; both narrations repeated it | output never compared to source |

Read 5 and 6 together with 1–4: **"28 tests passing" is what allowed the rest to
persist.** The suite is green, and it measures a layer nothing feeds and nobody
calls.

## 3. Why every existing gate missed all eight

| Gate | What it actually checks | Why it passes |
|---|---|---|
| `tsc` | types against types | `db:backup` is a string in JSON — invisible to the compiler |
| `jest` | code against fixtures the test wrote | a test cannot disagree with its own literal |
| `validate-config` | required fields present, no duplicate ids | it was written to check shape, and shape is intact |
| code review | the diff | the gap is an **absence**, and absences do not appear in diffs |
| `bd close` | that someone says it is done | closing asks nothing about demonstration |

Every one checks internal consistency. None checks correspondence. That is the
hole, and it is a hole of the same shape in five different places.

## 4. The sweep — six checks that surface the class

One script, run on demand and on a patrol. Each check emits a finding with its
evidence, never a verdict: a finding is a prompt to look.

1. **Declared-vs-absent.** Every declared command — `package.json` scripts,
   CLAUDE.md tables, README command blocks — must have a target file that
   exists, and where safe must exit 0 on `--help` or a dry run. *Catches #1.*
2. **Empty store.** Every table in every database: row count, last write. Flag
   any table a writer targets that holds 0 rows, or whose newest row predates
   the last commit touching its writer. *Catches #3.*
3. **Orphan surface.** Every route path, CLI entry and exported service method:
   look for a caller in this repo and in sibling repos, with `command grep -r`
   so gitignored paths are seen. Flag zero-caller surfaces. *Catches #4.*
4. **Tautological test.** Test files where no symbol imported from `src/` is
   ever invoked, or where every assertion's subject was constructed in the same
   block. *Catches #6.*
5. **Retired-premise residue.** Against the retirement register below, flag any
   live code, config, document or test that still names a retired premise.
   *Catches #2, and would have caught #7 before anyone wrote the bead.*
6. **Unstamped output.** Every family of generated artifacts must carry a
   verification stamp naming what the output was checked against. Flag families
   that have none. *Catches #8.*

Checks 1–4 are cheap and fully mechanical, and they have six known findings to
validate against — a detector that cannot re-find these is not working yet.

## 5. The retirement register

This enterprise retires by ruling: Playwright (dr-4ov), the TypeScript scrape
stack (dr-4td), the `/checkpoint` auto-save loop — retired in July precisely
because it was *"write-only, nothing reads it"* (co-59ywf). The ruling gets
recorded. **The residue does not.** Specimen #2 is a validator still cheerfully
confirming a cookie file for a browser nobody drives.

`docs/retired/REGISTER.md`: one row per retirement — what, ruling date, bead,
and the column that matters, **the premises it invalidates**. For dr-4ov that
column reads: cookies, headless mode, scroll cadence, DOM selectors, Discord
message ids, author ids, message URLs.

Check 5 reads that column. A ruling stops being a memory and becomes an
enforceable invariant. It is also the cheapest possible fix for #7 — dr-5f2
assumes message ids and message URLs, and both are on dr-4ov's invalidated list.

## 6. The guard on new work

This repository already refuses unverified claims — **on the analyst side.**
Capture dossiers say "frame-verified." yt-analyst cards mark every finding
verified and say how: arithmetic, frames, or both. Its export contract refuses
to synthesize an id the source cannot supply. Strader reports measured
quantities and names the mechanism story as narrative.

The code side never adopted the doctrine the same repository applies to its own
dossiers. The guard is to extend it, not to invent it:

**No bead closes without a `Demonstrated:` line**, carrying three parts:

- **what was run** — the exact command;
- **against what real input** — a path to something a collector produced, not a
  fixture;
- **what the output was compared to** — independently.

"Tests pass" is not a demonstration. It is the thing that failed here.
"Ran `dread.py ingest` on capture 20260912-103808 and checked all 8 messages
against the video frames" is one.

For code specifically: **any new table, endpoint or CLI command ships with one
test that feeds it real produced data from an artifact path.** One is enough.
The point is contact, not coverage.

## 7. Sequencing

1. Write `docs/retired/REGISTER.md` — two live rulings, an hour's work.
2. Build checks 1–4 as one script. Validate it by re-finding specimens 1, 3, 4
   and 6. File what else it finds.
3. Add the `Demonstrated:` close criterion to `.claude/rules/beads-first.md`,
   with a hook that refuses a close without it.
4. Check 5 once the register exists; check 6 once each artifact family declares
   its stamp field.
5. Offer the sweep and the convention to COO as a patrol formula in the idiom of
   the existing dogs. `mol-dog-stale-db` is already one instance of this class —
   a stale database is an empty store that nobody noticed — so the generalization
   has precedent and a home.

## 8. Non-goals

- **Not "write more tests."** The suite is green. More green would hide more.
- **Not deleting the idle layer.** That nothing demonstrates it is a finding;
  whether to keep it is a separate decision, and Steve's.
- **Not ceremony.** One line at close, one real-input test per new surface. If
  the guard costs more than that, it will be routed around, and a routed-around
  guard is itself a semantic gap.
