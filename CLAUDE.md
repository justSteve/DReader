# DReader

DReader is a Discord intelligence collector — a zgent (in-process toward Zgent certification) that scrapes, stores, and serves Discord channel data for the Gas Town enterprise. Other zgents query DReader for Discord context: conversation history, thread reconstructions, channel metadata.

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

## Graduation Status

DReader is on the path to Zgent certification. Current progress:

- **Source restored** from pre-restructure commit (gt-dr1.1, closed)
- **Structured logging** implemented — JSONL file + stderr transports, child loggers, level filtering (gt-dr1.4, closed)
- **JSONL narrative logging** — next step, extends structured logging with another transport (gt-dr1.2, open)
- **MCP server** — expose query API as MCP tools so sibling zgents can call DReader directly (gt-dr1.3, open)
- **Standard artifacts deployed** — beads-first, zgent-permissions, .gitignore, Python setup

## Key Commands

```bash
npm run dev          # Start API server
npm run test         # Run Jest tests
npm run auth-setup   # Configure Discord auth
npm run init-db      # Initialize SQLite database
npm run db:reset     # Reset database
```

## Conventions

- Beads-first: self-bead for non-trivial work, reference bead ID in commits
- Structured logging: use `createLogger('component')` not `console.log`
- Enterprise permissions: read sibling repos, write only own path
