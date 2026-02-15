import { createLogger, LogEntry, Transport } from '../logger';

describe('Logger', () => {
  let entries: LogEntry[];
  let capture: Transport;

  beforeEach(() => {
    entries = [];
    capture = (entry: LogEntry) => entries.push(entry);
  });

  it('writes structured JSONL entries', () => {
    const log = createLogger({ component: 'test', transports: [capture] });
    log.info('hello world', { key: 'value' });

    expect(entries).toHaveLength(1);
    expect(entries[0].level).toBe('info');
    expect(entries[0].component).toBe('test');
    expect(entries[0].message).toBe('hello world');
    expect(entries[0].data).toEqual({ key: 'value' });
    expect(entries[0].timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it('respects log level filtering', () => {
    const log = createLogger({ component: 'test', level: 'warn', transports: [capture] });
    log.debug('should not appear');
    log.info('should not appear');
    log.warn('should appear');
    log.error('should appear');

    expect(entries).toHaveLength(2);
    expect(entries[0].level).toBe('warn');
    expect(entries[1].level).toBe('error');
  });

  it('creates child loggers with dotted component names', () => {
    const log = createLogger({ component: 'scrape', transports: [capture] });
    const child = log.child('browser');
    child.info('navigating');

    expect(entries[0].component).toBe('scrape.browser');
  });

  it('omits data field when not provided', () => {
    const log = createLogger({ component: 'test', transports: [capture] });
    log.info('bare message');

    expect(entries[0].data).toBeUndefined();
  });

  it('sends to multiple transports', () => {
    const entries2: LogEntry[] = [];
    const capture2: Transport = (entry) => entries2.push(entry);

    const log = createLogger({ component: 'test', transports: [capture, capture2] });
    log.info('multi');

    expect(entries).toHaveLength(1);
    expect(entries2).toHaveLength(1);
  });
});
