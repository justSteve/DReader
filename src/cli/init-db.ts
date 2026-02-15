#!/usr/bin/env node

import DatabaseService from '../services/DatabaseService';
import * as path from 'path';
import { createLogger } from '../logging/logger';

const log = createLogger('cli.init-db');
const DB_PATH = path.join(process.cwd(), 'discord-scraper.db');

log.info('Initializing database', { dbPath: DB_PATH });
console.log('Initializing Discord Scraper database...');
console.log(`Database path: ${DB_PATH}`);

try {
  const db = new DatabaseService(DB_PATH);
  db.initialize();
  db.close();

  log.info('Database initialized');
  console.log('✓ Database initialized successfully');
  console.log('  - Tables created: servers, channels, messages, scrape_jobs');
  console.log('  - Indexes created for performance');
} catch (error) {
  log.error('Database initialization failed', { error: error instanceof Error ? error.message : String(error) });
  console.error('✗ Failed to initialize database:', error);
  process.exit(1);
}
