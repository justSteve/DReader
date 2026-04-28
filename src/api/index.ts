import express from 'express';
import cors from 'cors';
import serversRouter from './routes/servers';
import channelsRouter from './routes/channels';
import messagesRouter from './routes/messages';
import threadsRouter from './routes/threads';
import { createLogger } from '../logging/logger';

const log = createLogger('api');
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
  log.debug(`${req.method} ${req.path}`);
  next();
});

app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// Add domain routes
app.use('/api/servers', serversRouter);
app.use('/api/channels', channelsRouter);
app.use('/api/messages', messagesRouter);
app.use('/api/threads', threadsRouter);

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3001;

if (require.main === module) {
  app.listen(PORT, () => {
    log.info('Server started', { port: PORT });
  });
}

export default app;
