# DReader

Discord message archival system with thread reconstruction capabilities. Scrapes channels via browser automation and stores messages in SQLite for analysis.

## QuickStart

**Prerequisites:** Bun 1.3+, Claude Code CLI with `--chrome` flag

```bash
# 1. Clone and install
git clone https://github.com/justSteve/DReader.git
cd DReader
bun install

# 2. Start Claude Code with Chrome browser control
claude --chrome
# Log into Discord in the browser window that opens

# 3. Start the API server
bun run dev

# 4. Start scraping a channel
curl -X POST http://localhost:3001/api/scrape/start \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "YOUR_CHANNEL_ID", "scrape_type": "initialization"}'
```

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────┐
│ Claude Chrome       │────▶│ Scrape           │────▶│ SQLite DB   │
│ Extension           │     │ Orchestrator     │     │ (bun:sqlite)│
└─────────────────────┘     └──────────────────┘     └─────────────┘
         │                          │                       │
         │                          ▼                       ▼
    Browser DOM            ┌──────────────────┐     ┌─────────────┐
    Extraction             │ Hono REST API    │◀────│ Thread      │
                           │ :3001            │     │ Analyzer    │
                           └──────────────────┘     └─────────────┘
```

### Components

| Component | Purpose |
|-----------|---------|
| **ClaudeChromeController** | Browser automation via Claude's Chrome extension |
| **InitializationScrapeOrchestrator** | Historical scraping (backward paging) |
| **IncrementalScrapeOrchestrator** | New message scraping (forward paging) |
| **DatabaseService** | SQLite storage with bun:sqlite |
| **ThreadAnalyzer** | Reconstruct conversation trees from reply chains |

## Scrape Modes

### Initialization (Historical)
Scrapes backward in time to capture channel history.

```bash
# Full history
curl -X POST http://localhost:3001/api/scrape/start \
  -d '{"channel_id": "123", "scrape_type": "initialization"}'

# With date cutoff
curl -X POST http://localhost:3001/api/scrape/start \
  -d '{"channel_id": "123", "scrape_type": "initialization", "oldest_date_required": "2024-01-01"}'
```

### Incremental (New Messages)
Scrapes forward from last known message to capture new activity.

```bash
curl -X POST http://localhost:3001/api/scrape/start \
  -d '{"channel_id": "123", "scrape_type": "incremental"}'
```

## REST API

Base URL: `http://localhost:3001/api`

### Scrape Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/scrape/start` | Start new scrape job |
| `POST` | `/scrape/resume/:id` | Resume interrupted job |
| `GET` | `/scrape/status/:id` | Get job status |
| `GET` | `/scrape/channel/:id/status` | Get channel scrape status |

### Data Access
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/messages` | List messages (paginated) |
| `GET` | `/messages/:id` | Get single message |
| `GET` | `/servers` | List scraped servers |
| `GET` | `/channels` | List scraped channels |

### Thread Analysis (Deferred)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/threads/:id` | Get thread tree (returns 501) |

## Database Schema

SQLite database with these core tables:

| Table | Purpose |
|-------|---------|
| `servers` | Discord servers |
| `channels` | Discord channels |
| `messages` | Scraped messages with metadata |
| `scrape_jobs` | Job tracking with progress state |

### Key Columns in `scrape_jobs`
- `oldest_scraped_id` - Earliest message captured
- `newest_scraped_id` - Latest message captured
- `scrape_scope` - "initialization" or "incremental"
- `status` - pending, running, completed, failed

## Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3001 | API server port |
| `DB_PATH` | `./data/dreader.db` | SQLite database path |

### config.json
```json
{
  "scrape": {
    "scroll_delay_ms": 1000,
    "max_scrolls": 100,
    "messages_per_batch": 50
  }
}
```

## Project Structure

```
DReader/
├── src/
│   ├── api/                    # Hono REST API
│   │   ├── index.ts            # Server entry point
│   │   └── routes/             # Route handlers
│   ├── domain/
│   │   ├── scrape-engine/      # Browser control & orchestration
│   │   │   ├── ClaudeChromeController.ts
│   │   │   ├── InitializationScrapeOrchestrator.ts
│   │   │   └── IncrementalScrapeOrchestrator.ts
│   │   ├── metadata-capture/   # DOM extraction
│   │   ├── thread-reconstruction/  # Thread tree building
│   │   └── models/             # TypeScript types
│   ├── services/               # Database layer
│   │   ├── DatabaseService.ts
│   │   └── schema.sql
│   └── cli/                    # CLI tools
│       └── auth-setup.ts
├── packages/                   # Shared packages
├── tests/                      # Test suites
├── bunfig.toml                 # Bun configuration
└── package.json
```

## Development

```bash
# Install dependencies
bun install

# Run tests (50 passing, 11 skipped)
bun test

# Start dev server
bun run dev

# Type check
bun run typecheck
```

## Authentication

DReader uses Claude Code's Chrome browser for Discord authentication:

1. Start Claude Code with Chrome: `claude --chrome`
2. Navigate to Discord in the browser
3. Log in with your Discord account
4. Keep Claude Code running during scraping

No Discord bot token required - uses your browser session.

## Documentation

- [Code Review](docs/CODE_REVIEW.md) - Architecture assessment and recommendations
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) - Refactoring status and roadmap

## Limitations

- Thread analysis is deferred (returns 501)
- Requires Claude Code with `--chrome` flag
- Windows-focused (PowerShell scripts)
- No rate limiting on API endpoints yet

## Tech Stack

- **Runtime:** Bun 1.3+
- **API:** Hono
- **Database:** SQLite (bun:sqlite)
- **Browser:** Claude Chrome Extension
- **Language:** TypeScript (ESNext)
