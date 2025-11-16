# GymGenius Architecture

## Overview

GymGenius is a comprehensive fitness ecosystem built with a monorepo
architecture, supporting multiple client applications and a unified backend
infrastructure.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Client App  │  Trainer App │ Nutritionist │  Admin Panel   │
│  (Flutter)   │  (Flutter)   │    Panel     │   (Next.js)    │
│              │              │  (Next.js)   │                │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Real-time Layer                           │
├─────────────────────────────────────────────────────────────┤
│  Socket.io Server (Node.js) + Redis Adapter                 │
│  - Chat & Messaging                                          │
│  - Live workout tracking                                     │
│  - Real-time notifications                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Layer                                │
├─────────────────────────────────────────────────────────────┤
│  FastAPI (Python)                                            │
│  - RESTful API endpoints                                     │
│  - AI-powered workout/meal generation                        │
│  - Payment processing (Razorpay)                             │
│  - User management                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  PostgreSQL  │  Firestore   │    Redis     │  Firebase Auth │
│ (Structured) │    (Chat)    │   (Cache)    │   (Identity)   │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

## Technology Stack

### Backend

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL 15+ (transactional data)
- **Cache**: Redis 7+ (Socket.io adapter, caching)
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Real-time**: Socket.io (Node.js server)

### Mobile Apps (Flutter)

- **Language**: Dart 3.0+
- **Framework**: Flutter 3.16+
- **State Management**: Provider
- **Design System**: Kinetic Design System (Biometric Glow theme)
- **Real-time**: socket.io-client
- **HTTP**: http package

### Web Panels (React)

- **Language**: TypeScript 5.3+
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS 3.4
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts

### Authentication & Authorization

- **Provider**: Firebase Authentication
- **Strategy**: JWT tokens for API access
- **Roles**: Client, Trainer, Nutritionist, Admin, SuperAdmin

### Payments

- **Gateway**: Razorpay
- **Supported Methods**: PhonePe, Google Pay (UPI)
- **Features**: Retry logic (3 attempts), exponential backoff

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## Data Flow

### Authentication Flow

1. User signs in via Firebase Auth (email/password, Google, Apple)
2. Client receives Firebase ID token
3. Client sends ID token with each API request
4. Backend verifies token with Firebase Admin SDK
5. Backend returns user data from PostgreSQL

### Real-time Chat Flow

1. User authenticates Socket.io connection with Firebase token
2. User joins chat room: `chat:{chatId}`
3. Messages sent via Socket.io (ephemeral)
4. Messages persisted to Firestore (permanent storage)
5. Other participants receive message via Socket.io

### Payment Flow

1. User initiates payment (subscription, plan purchase)
2. Backend creates Razorpay order
3. Client displays Razorpay checkout (PhonePe/Google Pay)
4. User completes payment
5. Razorpay webhook notifies backend
6. Backend verifies signature
7. Backend updates payment status in PostgreSQL
8. Backend activates subscription

### Workout Generation Flow

1. User requests workout plan
2. Backend calls AI provider (OpenAI/Google Gemini)
3. AI generates personalized workout
4. Backend saves workout to PostgreSQL
5. Client receives workout data
6. User tracks progress (real-time via Socket.io)

## Security

### API Security

- Rate limiting: 20 req/min (chat), 10 req/min (generation)
- Input sanitization (HTML escape, XSS prevention)
- CORS policy (whitelisted origins)
- SQL injection prevention (parameterized queries)

### Authentication Security

- Firebase token verification on every request
- Role-based access control (RBAC)
- Secure password storage (Firebase handles)
- Token expiration: 30 minutes

### Data Security

- HTTPS/TLS everywhere
- Database encryption at rest
- Sensitive data redaction in logs
- Payment data handled by Razorpay (PCI-DSS compliant)

## Scalability

### Horizontal Scaling

- **Backend**: Stateless FastAPI instances behind load balancer
- **Socket.io**: Redis adapter enables multi-instance deployment
- **Database**: Read replicas for read-heavy operations

### Caching Strategy

- Redis for frequently accessed data (user profiles, config)
- CDN for static assets
- Socket.io adapter for distributed pub/sub

### Performance Optimizations

- Database connection pooling (10 connections, 20 max overflow)
- Async I/O throughout backend
- Image compression and lazy loading
- Pagination on all list endpoints

## Monitoring & Observability

### Metrics

- Request latency (p50, p95, p99)
- Error rates by endpoint
- Database query performance
- Socket.io connection count
- Payment success/failure rates

### Logging

- Structured JSON logs
- Trace IDs for request correlation
- Error stack traces
- User action audit logs

### Alerting

- API downtime > 1 minute
- Error rate > 5%
- Database connection pool exhausted
- Payment failures > 10/hour

## Disaster Recovery

### Backup Strategy

- PostgreSQL: Daily full backup, hourly incremental
- Firestore: Automatic daily exports to Cloud Storage
- Redis: AOF persistence enabled
- Retention: 30 days

### High Availability

- Multi-AZ database deployment
- Auto-scaling for compute resources
- Circuit breakers for external services
- Graceful degradation (AI generation failure)

## Development Workflow

### Local Development

```bash
# Backend
cd packages/backend
poetry install
poetry run uvicorn main:app --reload

# Socket.io
cd packages/backend/socketio
npm install
npm run dev

# Flutter Apps
cd apps/client-app
flutter pub get
flutter run

# React Panels
cd apps/nutritionist-panel
npm install
npm run dev
```

### Testing Strategy

- **Unit Tests**: pytest (backend), flutter test (mobile), Jest (web)
- **Integration Tests**: FastAPI TestClient, Flutter integration_test
- **E2E Tests**: Playwright (web panels)
- **Coverage Target**: 80%+

### Deployment Process

1. Developer pushes to `develop` branch
2. CI runs tests (path-filtered for affected apps)
3. Code review required
4. Merge to `main` triggers production deployment
5. Database migrations run automatically (Alembic)
6. Zero-downtime deployment (rolling updates)

## Future Enhancements

- [ ] Wearable device integration (Apple Watch, Fitbit)
- [ ] Video calling for trainer sessions (WebRTC)
- [ ] AI-powered meal photo recognition
- [ ] Gamification (badges, leaderboards)
- [ ] Social features (follow trainers, share workouts)
- [ ] Multi-language support (i18n)
- [ ] Offline mode (local SQLite cache)
