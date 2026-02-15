import * as fs from 'fs';
import * as path from 'path';

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  component: string;
  message: string;
  data?: Record<string, unknown>;
}

export interface Logger {
  debug(message: string, data?: Record<string, unknown>): void;
  info(message: string, data?: Record<string, unknown>): void;
  warn(message: string, data?: Record<string, unknown>): void;
  error(message: string, data?: Record<string, unknown>): void;
  child(component: string): Logger;
}

export type Transport = (entry: LogEntry) => void;

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

/**
 * Create a JSONL file transport that appends log entries to a file.
 * Creates the directory if it doesn't exist.
 */
export function createFileTransport(logDir: string): Transport {
  fs.mkdirSync(logDir, { recursive: true });

  // One file per day: dreader-2026-02-15.jsonl
  let currentDate = '';
  let fd: number | null = null;

  function getFd(): number {
    const today = new Date().toISOString().slice(0, 10);
    if (today !== currentDate || fd === null) {
      if (fd !== null) {
        fs.closeSync(fd);
      }
      currentDate = today;
      const filePath = path.join(logDir, `dreader-${today}.jsonl`);
      fd = fs.openSync(filePath, 'a');
    }
    return fd;
  }

  return (entry: LogEntry) => {
    const line = JSON.stringify(entry) + '\n';
    fs.writeSync(getFd(), line);
  };
}

/**
 * Create a stderr transport for console output.
 * Compact single-line format for human readability.
 */
export function createConsoleTransport(): Transport {
  return (entry: LogEntry) => {
    const time = entry.timestamp.slice(11, 19);
    const lvl = entry.level.toUpperCase().padEnd(5);
    const ctx = entry.data ? ` ${JSON.stringify(entry.data)}` : '';
    process.stderr.write(`${time} ${lvl} [${entry.component}] ${entry.message}${ctx}\n`);
  };
}

class LoggerImpl implements Logger {
  constructor(
    private component: string,
    private minLevel: LogLevel,
    private transports: Transport[],
  ) {}

  debug(message: string, data?: Record<string, unknown>): void {
    this.log('debug', message, data);
  }

  info(message: string, data?: Record<string, unknown>): void {
    this.log('info', message, data);
  }

  warn(message: string, data?: Record<string, unknown>): void {
    this.log('warn', message, data);
  }

  error(message: string, data?: Record<string, unknown>): void {
    this.log('error', message, data);
  }

  child(component: string): Logger {
    return new LoggerImpl(
      `${this.component}.${component}`,
      this.minLevel,
      this.transports,
    );
  }

  private log(level: LogLevel, message: string, data?: Record<string, unknown>): void {
    if (LOG_LEVELS[level] < LOG_LEVELS[this.minLevel]) return;

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      component: this.component,
      message,
    };
    if (data !== undefined) {
      entry.data = data;
    }

    for (const transport of this.transports) {
      transport(entry);
    }
  }
}

export interface LoggerOptions {
  component: string;
  level?: LogLevel;
  logDir?: string;
  console?: boolean;
  transports?: Transport[];
}

/**
 * Create a logger instance.
 *
 * Default behavior:
 * - Writes JSONL to data/logs/
 * - Also writes to stderr in development
 * - Level controlled by LOG_LEVEL env var (default: info)
 */
export function createLogger(opts: string | LoggerOptions): Logger {
  const options: LoggerOptions = typeof opts === 'string' ? { component: opts } : opts;

  const level = options.level
    ?? (process.env.LOG_LEVEL as LogLevel | undefined)
    ?? 'info';

  const logDir = options.logDir ?? path.join(process.cwd(), 'data', 'logs');
  const useConsole = options.console ?? (process.env.NODE_ENV !== 'test');

  const transports: Transport[] = options.transports ?? [];

  // Default transports if none provided
  if (transports.length === 0) {
    transports.push(createFileTransport(logDir));
    if (useConsole) {
      transports.push(createConsoleTransport());
    }
  }

  return new LoggerImpl(options.component, level, transports);
}
