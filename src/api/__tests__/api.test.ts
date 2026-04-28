import request from 'supertest';
import DatabaseService from '../../services/DatabaseService';
import * as fs from 'fs';

const TEST_DB = './test-api.db';

describe('API Integration Tests', () => {
  let db: DatabaseService;
  let app: any;

  beforeAll(() => {
    if (fs.existsSync(TEST_DB)) {
      fs.unlinkSync(TEST_DB);
    }

    process.env.DB_PATH = TEST_DB;

    db = new DatabaseService(TEST_DB);
    db.initialize();

    db.insertServer({ id: 'server_1', name: 'Test Server' });
    db.insertChannel({ id: 'channel_1', server_id: 'server_1', name: 'general', message_count: 0 });

    app = require('../index').default;
  });

  afterAll(() => {
    db.close();
    if (fs.existsSync(TEST_DB)) {
      fs.unlinkSync(TEST_DB);
    }
  });

  describe('GET /api/health', () => {
    it('should return health status', async () => {
      const res = await request(app).get('/api/health');
      expect(res.status).toBe(200);
      expect(res.body.status).toBe('ok');
    });
  });

  describe('GET /api/servers', () => {
    it('should list all servers', async () => {
      const res = await request(app).get('/api/servers');
      expect(res.status).toBe(200);
      expect(res.body).toHaveLength(1);
      expect(res.body[0].name).toBe('Test Server');
    });
  });
});
