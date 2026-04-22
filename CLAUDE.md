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

## Constraint: No Discord API Access

DReader has no access to the Discord API — no bot token, no OAuth app, no REST endpoints. This is a permanent constraint, not a gap to be filled. All message retrieval must work through computer-use: automating the Discord desktop app (pywinauto) or browser-based UI (DOM scraping). Do not propose or build solutions that assume API access.

## Architecture

**Dual-language**: TypeScript (API, scrape engine, storage) + Python (keyboard-driven retrieval, clipboard automation)

### TypeScript Core

| Layer | Path | Purpose |
|-------|------|---------|
| API | `src/api/` | Express REST server — channels, messages, threads, scrape jobs |
| Scrape Engine | `src/domain/scrape-engine/` | Browser orchestrator, message scrolling, DOM selectors |
| Thread Reconstruction | `src/domain/thread-reconstruction/` | ThreadAnalyzer — rebuilds conversation threads from flat messages |
| Storage | `src/services/` | DatabaseService (better-sqlite3), schema.sql |
| Logging | `src/logging/` | Structured JSONL logger — transport-based, daily rotation, zero deps |
| CLI | `src/cli/` | auth-setup, init-db, validate-config, db-reset |

### Python Retrieval (`src/retrieval/`)

Keyboard-driven message retrieval that automates the Discord desktop app via pywinauto — no unofficial APIs. Clipboard-based extraction, session management, window control.

## What Every Claude Instance Must Understand

1. **Beads-first is non-negotiable.** Read the gate at the top of this file. Use `bd` commands. No exceptions.
2. **Service provider role.** DReader exists to serve other agents with Discord intel. See `.claude/rules/zgent-permissions.md`.
3. **No Discord API.** All retrieval is computer-use (pywinauto, DOM scraping). Never propose API-based solutions.
4. **Structured logging.** Use `createLogger('component')` not `console.log`.

## Key Commands

```bash
npm run dev          # Start API server
npm run test         # Run Jest tests
npm run auth-setup   # Configure Discord auth
npm run init-db      # Initialize SQLite database
npm run db:reset     # Reset database
bd ready             # Find available work
bd show <id>         # View issue details
bd update <id> --claim  # Claim work
bd close <id>        # Complete work
bd prime             # Re-read PRIME.md (context for new sessions)
```

## Key Files

| Path | Purpose |
|------|---------|
| `src/api/` | Express REST server |
| `src/domain/scrape-engine/` | Browser orchestrator |
| `src/domain/thread-reconstruction/` | Thread rebuilder |
| `src/services/` | DatabaseService, schema |
| `src/logging/` | Structured JSONL logger |
| `src/retrieval/` | Python keyboard-driven retrieval |
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
