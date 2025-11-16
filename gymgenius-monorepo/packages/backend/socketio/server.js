import { createAdapter } from '@socket.io/redis-adapter';
import dotenv from 'dotenv';
import * as admin from 'firebase-admin';
import fs from 'node:fs';
import { createClient } from 'redis';
import { Server } from 'socket.io';

dotenv.config({ path: '../.env' });

// Initialize Firebase Admin
const serviceAccountPath = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;
if (serviceAccountPath) {
  try {
    const credentials = fs.readFileSync(serviceAccountPath, 'utf8');
    const serviceAccount = JSON.parse(credentials);
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
    });
  } catch (err) {
    console.warn(
      'Unable to initialize Firebase Admin with provided service account path:',
      err.message
    );
  }
}

// Initialize Socket.io server
const io = new Server(
  Number.parseInt(process.env.SOCKETIO_PORT || '3001', 10),
  {
    cors: {
      origin: process.env.SOCKETIO_CORS_ORIGINS?.split(',') || [
        'http://localhost:3000',
      ],
      credentials: true,
    },
  }
);

// Redis adapter for horizontal scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await pubClient.connect();
await subClient.connect();
io.adapter(createAdapter(pubClient, subClient));
console.warn('Redis adapter initialized');

// Authentication middleware
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;

  if (!token) {
    return next(new Error('Authentication token required'));
  }

  try {
    const decodedToken = await admin.auth().verifyIdToken(token);
    socket.data.user = {
      uid: decodedToken.uid,
      email: decodedToken.email,
    };
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    next(new Error('Invalid authentication token'));
  }
});

// Connection handler
io.on('connection', (socket) => {
  console.warn(`User connected: ${socket.data.user.uid}`);

  // Join user's personal room
  socket.join(`user:${socket.data.user.uid}`);

  // Join chat room
  socket.on('join_chat', (chatId) => {
    socket.join(`chat:${chatId}`);
    console.warn(`User ${socket.data.user.uid} joined chat: ${chatId}`);
  });

  // Leave chat room
  socket.on('leave_chat', (chatId) => {
    socket.leave(`chat:${chatId}`);
    console.warn(`User ${socket.data.user.uid} left chat: ${chatId}`);
  });

  // Send message
  socket.on('send_message', (data) => {
    const { chatId, message, timestamp } = data;

    // Broadcast to chat room
    io.to(`chat:${chatId}`).emit('new_message', {
      chatId,
      message,
      sender: socket.data.user,
      timestamp,
    });
  });

  // Typing indicator
  socket.on('typing_start', (chatId) => {
    socket.to(`chat:${chatId}`).emit('user_typing', {
      chatId,
      user: socket.data.user,
    });
  });

  socket.on('typing_stop', (chatId) => {
    socket.to(`chat:${chatId}`).emit('user_stopped_typing', {
      chatId,
      user: socket.data.user,
    });
  });

  // Workout tracking events
  socket.on('workout_started', (data) => {
    const { workoutId, timestamp } = data;

    // Notify trainers/nutritionists monitoring this user
    io.to(`user:${socket.data.user.uid}`).emit('workout_status', {
      status: 'started',
      workoutId,
      timestamp,
    });
  });

  socket.on('workout_completed', (data) => {
    const { workoutId, duration, caloriesBurned, timestamp } = data;

    io.to(`user:${socket.data.user.uid}`).emit('workout_status', {
      status: 'completed',
      workoutId,
      duration,
      caloriesBurned,
      timestamp,
    });
  });

  // Real-time notifications
  socket.on('notification', (data) => {
    const { targetUserId, notification } = data;

    io.to(`user:${targetUserId}`).emit('notification_received', {
      ...notification,
      timestamp: new Date().toISOString(),
    });
  });

  // Disconnect handler
  socket.on('disconnect', (reason) => {
    console.warn(
      `User disconnected: ${socket.data.user.uid} - Reason: ${reason}`
    );
  });

  // Error handler
  socket.on('error', (error) => {
    console.error(`Socket error for user ${socket.data.user.uid}:`, error);
  });
});

// Global error handler
io.engine.on('connection_error', (error) => {
  console.error('Connection error:', error);
});

console.warn(
  `Socket.io server running on port ${process.env.SOCKETIO_PORT || 3001}`
);

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.warn('SIGTERM received, closing server...');
  await Promise.all([io.close(), pubClient.quit(), subClient.quit()]);
  process.exit(0);
});
