# DReader — Enterprise Discord Intelligence Service

**Zgent Status:** Zgent (certified)
**Role:** Service provider — external intel collector serving Discord data to sibling zgents
**Bead Prefix:** `dr`

## STOP — Beads Gate (Read This First)

**This repo is beads-first. You MUST authorize work before doing it.**

Before making ANY substantive changes (creating/modifying files, installing deps, changing config), do this:

```bash
bd ready                    # See if there is already an open bead for this work
bd create --title "Short title"  # Create one if not — YOU own this, do not ask the user
bd update <id> --status in_progress  # Claim it
```

When done:
```bash
bd close <id>               # Mark complete
```

Reference the bead ID in your commit messages: `[dr-xxx] description`.

**No bead = no work.** Minor housekeeping (typos, status fields) is exempt. Everything else gets a bead. If in doubt, create one — it is cheap. See `.claude/rules/beads-first.md` for the full rule.

**This is not optional. This is how THIS repo works, every session, every instance.**

## What This Is

DReader is a Discord intelligence collector that scrapes, stores, and serves Discord channel data for the Gas City enterprise. Other zgents query DReader for Discord context: conversation history, thread reconstructions, channel metadata.

## Mission

Collect information from Discord channels and make it queryable by sibling zgents. DReader publishes its query API according to shared enterprise conventions so any zgent in the ecosystem can discover and use it.

## Asking Steve

If the agent can decide it, it decides, does it, and reports. When something
genuinely needs Steve: one sentence with a recommended answer he can accept in
a word, then stop. **Silence means Deferred, never Yes** (Steve, 2026-09-12,
global rule for every agent): an unanswered ask stays open on its bead and
nobody proceeds on it.

## Constraint: No Discord API Access, No Account Automation

DReader has no access to the Discord API — no bot token, no OAuth app, no REST endpoints. This is a permanent constraint, not a gap to be filled. Do not propose or build solutions that assume API access.

Browser automation of Steve's account (Playwright/Selenium DOM scraping) was **retired by Steve on 2026-09-12** (dr-4ov). Retrieval is now **screen capture**: Steve pages through Discord on his own screen, Game Bar records it, and Gemini transcribes the video (`discord-reader/`). Do not propose reviving the scraper; the code is preserved at git tag `playwright-retired` if that ruling is ever reversed.

## Architecture

Collection is `discord-reader/` (Python: screen-capture video → Gemini → transcript dossiers on disk). The query/serve layer is TypeScript (Express + SQLite). **They are not yet connected**: transcripts do not reach the database. Bridging them is the open architectural need.

### TypeScript Query Layer

| Layer | Path | Purpose |
|-------|------|---------|
| API | `src/api/` | Express REST server for channels, messages, threads (read-only query surface) |
| Thread Reconstruction | `src/domain/thread-reconstruction/` | ThreadAnalyzer — rebuilds conversation threads from flat messages |
| Storage | `src/services/` | DatabaseService (better-sqlite3), schema.sql |
| Logging | `src/logging/` | Structured JSONL logger — transport-based, daily rotation, zero deps |
| CLI | `src/cli/` | init-db, validate-config, db-reset, db-backup |

### Collection (`discord-reader/`)

`dread.py` ingests a Game Bar capture of a paged-through Discord channel, uploads it to Gemini Flash at high media resolution, and writes `transcript.json` / `transcript.md` / `CARD.md` into `discord-reader/captures/<id>/` (gitignored: private). Doctrine, verification procedure and lessons live in `discord-reader/CLAUDE.md` and `discord-reader/LESSONS.md`. Forum channels: each post is a thread and is captured on its own.

## What Every Claude Instance Must Understand

1. **Beads-first is non-negotiable.** Read the gate at the top of this file. Use `bd` commands. No exceptions.
2. **Service provider role.** DReader exists to serve other agents with Discord intel. See `.claude/rules/zgent-permissions.md`.
3. **No Discord API, no account automation.** Retrieval is Steve's screen captures transcribed by Gemini. Never propose API-based or browser-automation solutions.
4. **Structured logging.** Use `createLogger('component')` not `console.log`.

## Key Commands

```bash
npm run dev          # Start API server (Express, query layer)
npm run test         # Run Jest tests (TypeScript)
npm run init-db      # Initialize SQLite database
npm run db:reset     # Reset database
cd discord-reader && .venv/bin/python dread.py ingest --label "server/channel"   # transcribe newest capture
cd discord-reader && .venv/bin/python dread.py env                                # credential check
bd ready             # Find available work
bd show <id>         # View issue details
bd update <id> --claim  # Claim work
bd close <id>        # Complete work
bd prime             # Re-read PRIME.md (context for new sessions)
```

## Key Files

| Path | Purpose |
|------|---------|
| `src/api/` | Express REST server (read-only query surface) |
| `src/domain/thread-reconstruction/` | Thread rebuilder |
| `src/services/` | DatabaseService, schema |
| `src/logging/` | Structured JSONL logger |
| `discord-reader/` | Screen-capture → Gemini transcription (Python), capture dossiers |
| `docs/retired/` | Retired browser-automation track: findings kept, code at tag `playwright-retired` |
| `.beads/` | Beads (work authorization) |

## Session Completion

When ending a work session:

1. File any remaining work as beads
2. Run quality gates if code changed
3. Update or close beads
4. Commit and push — **work is NOT done until `git push` succeeds**
5. Run `/handoff` to append to `DaysActivity.md`

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for short facts that must be injected into EVERY session at `bd prime` — keep it small; it is a context tax on every session

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
