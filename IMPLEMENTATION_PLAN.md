# DReader Refactoring Plan

## Overview
Refactor Discord scraper at `/home/gtuser/gt/DReader/mayor/rig` with:
1. Two distinct scrape scopes (initialization vs incremental)
2. Bun runtime migration
3. Claude Chrome Extension for browser control (NO Playwright)
4. Deferred thread analysis

---

## Implementation Status

### Phase 1: Foundation ✅ COMPLETE
- [x] Update types.ts with ScrapeScope, InitializationScrapeOptions, IncrementalScrapeOptions
- [x] Create BrowserControllerInterface.ts
- [x] Update schema.sql with tracking columns (oldest_scraped_id, etc.)

### Phase 2: Database ✅ COMPLETE
- [x] Migrate to bun:sqlite
- [x] Add new methods: getOldestMessageInChannel, getNewestMessageInChannel, updateScrapeJobProgress, createInitializationJob, createIncrementalJob, isChannelFullyInitialized

### Phase 3: Browser Controllers ✅ COMPLETE
- [x] Create ClaudeChromeController.ts (file-based command protocol)
- [x] ~~Refactor DiscordBrowserController.ts~~ DEPRECATED - Playwright removed
- [x] Add scrollUp(), scrollDown(), extractVisibleMessages(), navigateToMessage() methods

### Phase 4: Orchestrators ✅ COMPLETE
- [x] Create InitializationScrapeOrchestrator.ts (backward paging)
- [x] Create IncrementalScrapeOrchestrator.ts (forward paging, new-only)
- [x] Resume capability for interrupted jobs

### Phase 5: API ✅ COMPLETE
- [x] Migrate from Express to Hono
- [x] Update scrape routes with new scrape types
- [x] Add channel status endpoint
- [x] Defer thread routes (501)

### Phase 6: Runtime ✅ COMPLETE
- [x] Update package.json for Bun (Playwright removed)
- [x] Update tsconfig.json for ESNext/bundler
- [x] Create bunfig.toml
- [x] Delete jest.config.js

### Phase 7: Integration ✅ COMPLETE
- [x] Install Bun runtime (v1.3.6)
- [x] Run `bun install` - dependencies installed
- [x] Run `bun test` - 50 passing, 11 skipped, 0 failures
- [x] Migrate tests from Jest to bun:test
- [x] Remove Playwright dependency
- [ ] Test initialization scrape flow (requires Claude Code --chrome)
- [ ] Test incremental scrape flow (requires Claude Code --chrome)
- [ ] Test resume capability (requires Claude Code --chrome)

#### Test Migration Notes (2026-01-16)
- Migrated all tests from Jest to bun:test per overseer directive
- Tests using `jest.mock()` converted to `mock.module()` and plain mock objects
- ThreadAnalyzer tests marked as skipped (feature deferred)
- Browser integration tests require Claude Code with --chrome flag (NOT Playwright)
- API tests use mock orchestrators to avoid browser dependencies

#### Playwright Removal (2026-01-16)
- Removed `playwright` from package.json dependencies
- Deprecated `DiscordBrowserController.ts` (renamed to .deprecated)
- Deprecated `ScrapeOrchestrator.ts` (renamed to .deprecated)
- Updated orchestrators to use only `ClaudeChromeController`
- Updated `types.ts` to remove `headless` and `browser_controller` options
- Updated `auth-setup.ts` CLI to show new authentication flow

---

## Files Changed

### Created
- `src/domain/scrape-engine/BrowserControllerInterface.ts`
- `src/domain/scrape-engine/ClaudeChromeController.ts`
- `src/domain/scrape-engine/InitializationScrapeOrchestrator.ts`
- `src/domain/scrape-engine/IncrementalScrapeOrchestrator.ts`
- `bunfig.toml`
- `test-setup.ts`

### Modified
- `src/domain/models/types.ts` - Added ScrapeScope types, updated DiscordConfig (no Playwright)
- `src/services/schema.sql` - Added tracking columns to scrape_jobs
- `src/services/DatabaseService.ts` - Migrated to bun:sqlite, added new methods
- `src/api/index.ts` - Migrated to Hono
- `src/api/routes/*.ts` - Migrated to Hono
- `src/domain/thread-reconstruction/ThreadAnalyzer.ts` - Stubbed (deferred)
- `package.json` - Bun scripts and dependencies (no Playwright)
- `tsconfig.json` - ESNext configuration
- `src/cli/auth-setup.ts` - Updated for Claude Chrome auth flow

### Deprecated
- `src/domain/scrape-engine/DiscordBrowserController.ts.deprecated`
- `src/domain/scrape-engine/ScrapeOrchestrator.ts.deprecated`

### Deleted
- `jest.config.js`
- `src/domain/scrape-engine/APIScrapeOrchestrator.ts`

---

## Usage Examples

### Authentication (with Claude Chrome Extension)
```bash
# Start Claude Code with Chrome browser
claude --chrome

# Log into Discord in the browser window
# Keep Claude Code running during scraping operations
```

### Initialization Scrape (historical)
```bash
curl -X POST http://localhost:3001/api/scrape/start \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "123", "scrape_type": "initialization"}'

# With date cutoff
curl -X POST http://localhost:3001/api/scrape/start \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "123", "scrape_type": "initialization", "oldest_date_required": "2024-01-01"}'
```

### Incremental Scrape (new only)
```bash
curl -X POST http://localhost:3001/api/scrape/start \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "123", "scrape_type": "incremental"}'
```

### Resume Interrupted Job
```bash
curl -X POST http://localhost:3001/api/scrape/resume/123
```

### Check Channel Status
```bash
curl http://localhost:3001/api/scrape/channel/123/status
```

---

## Next Steps
1. ~~Install Bun: `curl -fsSL https://bun.sh/install | bash`~~ ✅ Done
2. ~~Install dependencies: `cd DReader/mayor/rig && bun install`~~ ✅ Done
3. ~~Run tests: `bun test`~~ ✅ Done (50 pass, 11 skip)
4. ~~Remove Playwright dependency~~ ✅ Done
5. Start Claude Code with Chrome: `claude --chrome`
6. Start server: `bun run dev`
7. Test with a real Discord channel
