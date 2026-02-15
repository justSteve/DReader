#!/usr/bin/env node

import DatabaseService from '../services/DatabaseService';
import * as path from 'path';
import * as fs from 'fs';
import { createLogger } from '../logging/logger';

const log = createLogger('cli.db-reset');
const DB_PATH = path.join(process.cwd(), 'discord-scraper.db');

log.info('Resetting database', { dbPath: DB_PATH });
console.log('Resetting Discord Scraper database...');
console.log(`Database path: ${DB_PATH}`);

try {
  if (fs.existsSync(DB_PATH)) {
    fs.unlinkSync(DB_PATH);
    console.log('✓ Deleted existing database');
  }

  const db = new DatabaseService(DB_PATH);
  db.initialize();
  db.close();

  log.info('Database reset complete');
  console.log('✓ Database reset successfully');
  console.log('  - Tables created: servers, channels, messages, scrape_jobs');
  console.log('  - Schema updated with composite primary key and new fields');
  console.log('  - Indexes created for performance');
} catch (error) {
  log.error('Database reset failed', { error: error instanceof Error ? error.message : String(error) });
  console.error('✗ Failed to reset database:', error);
  process.exit(1);
}
