# GymGenius Deployment Guide

## Prerequisites

- Docker 24+
- Kubernetes 1.28+ (production)
- PostgreSQL 15+
- Redis 7+
- Firebase project with Authentication enabled
- Razorpay account

## Environment Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/gymgenius
REDIS_URL=redis://host:6379/0

# Security
SECRET_KEY=your-256-bit-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Providers
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
AI_PROVIDER=openai

# Razorpay
RAZORPAY_KEY_ID=rzp_live_...
RAZORPAY_KEY_SECRET=...

# Firebase
FIREBASE_SERVICE_ACCOUNT_PATH=/path/to/service-account.json

# Socket.io
SOCKETIO_PORT=3001
SOCKETIO_CORS_ORIGINS=https://app.gymgenius.com,https://admin.gymgenius.com

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Flutter Apps (.env)

```bash
API_BASE_URL=https://api.gymgenius.com
SOCKET_URL=https://socket.gymgenius.com
```

### React Panels (.env.production)

```bash
NEXT_PUBLIC_API_BASE_URL=https://api.gymgenius.com
NEXT_PUBLIC_SOCKET_URL=https://socket.gymgenius.com
```

## Database Setup

### Create Database

```bash
# PostgreSQL
createdb gymgenius_production

# Run migrations
cd packages/backend
poetry run alembic upgrade head
```

### Seed Data (Production)

```sql
-- Create superadmin account
INSERT INTO users (id, firebase_uid, email, full_name, role, is_active)
VALUES (
  gen_random_uuid(),
  'firebase-uid-from-console',
  'superadmin@gymgenius.com',
  'System Administrator',
  'superadmin',
  true
);

-- Create admin account
INSERT INTO users (id, firebase_uid, email, full_name, role, is_active)
VALUES (
  gen_random_uuid(),
  'firebase-uid-from-console',
  'admin@gymgenius.com',
  'Admin User',
  'admin',
  true
);
```

## Docker Deployment

### Build Images

```bash
# Backend
cd packages/backend
docker build -t gymgenius-backend:latest .

# Socket.io
cd packages/backend/socketio
docker build -t gymgenius-socketio:latest .

# React Panels
cd apps/nutritionist-panel
docker build -t gymgenius-nutritionist:latest .

cd apps/admin-panel
docker build -t gymgenius-admin:latest .
```

### Docker Compose (Development/Staging)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: gymgenius
      POSTGRES_USER: gymgenius
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  redis:
    image: redis:7
    ports:
      - '6379:6379'

  backend:
    image: gymgenius-backend:latest
    environment:
      DATABASE_URL: postgresql://gymgenius:${DB_PASSWORD}@postgres:5432/gymgenius
      REDIS_URL: redis://redis:6379/0
    ports:
      - '8000:8000'
    depends_on:
      - postgres
      - redis

  socketio:
    image: gymgenius-socketio:latest
    environment:
      REDIS_URL: redis://redis:6379/0
    ports:
      - '3001:3001'
    depends_on:
      - redis

volumes:
  postgres_data:
```

## Kubernetes Deployment (Production)

### Backend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gymgenius-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gymgenius-backend
  template:
    metadata:
      labels:
        app: gymgenius-backend
    spec:
      containers:
        - name: backend
          image: gymgenius-backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: gymgenius-secrets
                  key: database-url
          resources:
            requests:
              memory: '512Mi'
              cpu: '500m'
            limits:
              memory: '1Gi'
              cpu: '1000m'
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: gymgenius-backend
spec:
  selector:
    app: gymgenius-backend
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

### Socket.io Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gymgenius-socketio
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gymgenius-socketio
  template:
    metadata:
      labels:
        app: gymgenius-socketio
    spec:
      containers:
        - name: socketio
          image: gymgenius-socketio:latest
          ports:
            - containerPort: 3001
          env:
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: gymgenius-secrets
                  key: redis-url
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
---
apiVersion: v1
kind: Service
metadata:
  name: gymgenius-socketio
spec:
  selector:
    app: gymgenius-socketio
  ports:
    - port: 80
      targetPort: 3001
  type: LoadBalancer
```

## Flutter App Deployment

### Android (Google Play)

```bash
cd apps/client-app

# Build release APK
flutter build apk --release

# Build App Bundle
flutter build appbundle --release

# Upload to Google Play Console
```

### iOS (App Store)

```bash
cd apps/client-app

# Build iOS app
flutter build ios --release

# Open in Xcode
open ios/Runner.xcworkspace

# Archive and upload via Xcode
```

## React Panel Deployment

### Vercel (Recommended)

```bash
# Nutritionist Panel
cd apps/nutritionist-panel
vercel --prod

# Admin Panel
cd apps/admin-panel
vercel --prod
```

### Self-Hosted (Nginx)

```nginx
server {
    listen 80;
    server_name nutritionist.gymgenius.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Monitoring Setup

### Prometheus

```yaml
scrape_configs:
  - job_name: 'gymgenius-backend'
    static_configs:
      - targets: ['backend:8000']
```

### Grafana Dashboards

- API Request Rate
- Error Rate by Endpoint
- Database Query Performance
- Socket.io Connection Count
- Payment Success/Failure Rate

## Backup & Recovery

### PostgreSQL Backup

```bash
# Daily backup
pg_dump -h localhost -U gymgenius gymgenius_production > backup_$(date +%Y%m%d).sql

# Restore
psql -h localhost -U gymgenius gymgenius_production < backup_20240101.sql
```

### Firestore Backup

```bash
gcloud firestore export gs://gymgenius-backups/$(date +%Y%m%d)
```

## SSL/TLS Configuration

### Let's Encrypt (Certbot)

```bash
certbot --nginx -d api.gymgenius.com -d socket.gymgenius.com
```

## Scaling Strategy

### Horizontal Scaling

- **Backend**: Auto-scale based on CPU (target: 70%)
- **Socket.io**: Scale with Redis adapter (supports multiple instances)
- **Database**: Read replicas for read-heavy operations

### Vertical Scaling

- **Backend**: 2 vCPU, 4GB RAM (minimum)
- **Socket.io**: 1 vCPU, 2GB RAM (minimum)
- **PostgreSQL**: 4 vCPU, 8GB RAM (minimum)
- **Redis**: 2 vCPU, 4GB RAM (minimum)

## Rollback Procedure

```bash
# Kubernetes rollback
kubectl rollout undo deployment/gymgenius-backend

# Database migration rollback
cd packages/backend
poetry run alembic downgrade -1
```

## Health Checks

- **Backend**: `GET /health` (expect 200 OK)
- **Socket.io**: WebSocket connection test
- **Database**: `SELECT 1` query
- **Redis**: `PING` command

## Troubleshooting

### Backend not starting

1. Check environment variables
2. Verify database connection
3. Check logs: `kubectl logs deployment/gymgenius-backend`

### Socket.io connection failures

1. Verify Redis is running
2. Check CORS configuration
3. Test WebSocket connectivity

### Database migration failures

1. Check migration script syntax
2. Verify database permissions
3. Rollback and retry
