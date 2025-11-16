# 🚀 GymGenius Quick Start Guide

This guide will get you up and running with the GymGenius development
environment in minutes.

## Prerequisites

Ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 20+** - [Download](https://nodejs.org/)
- **Flutter 3.16+** -
  [Install Guide](https://docs.flutter.dev/get-started/install)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Redis 7+** - [Download](https://redis.io/download)
- **Poetry** - Run: `curl -sSL https://install.python-poetry.org | python3 -`

## Step 1: Clone & Navigate

```bash
cd /Users/morningstar/Downloads/fitai_-your-personal-fitness-coach/gymgenius-monorepo
```

## Step 2: Backend Setup

### 2.1 Install Dependencies

```bash
cd packages/backend
poetry install
```

### 2.2 Create Database

```bash
createdb gymgenius_dev
```

### 2.3 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/gymgenius_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-key
RAZORPAY_KEY_ID=rzp_test_your_key
RAZORPAY_KEY_SECRET=your_secret
```

### 2.4 Run Migrations

```bash
poetry run alembic upgrade head
```

### 2.5 Start Backend

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000 ✅ API docs:
http://localhost:8000/docs

## Step 3: Socket.io Server

### 3.1 Install Dependencies

```bash
cd packages/backend/socketio
npm install
```

### 3.2 Start Server

```bash
npm run dev
```

✅ Socket.io server running at: http://localhost:3001

## Step 4: Flutter Client App

### 4.1 Get Dependencies

```bash
cd apps/client-app
flutter pub get
```

### 4.2 Create .env File

```bash
echo "API_BASE_URL=http://localhost:8000" > .env
echo "SOCKET_URL=http://localhost:3001" >> .env
```

### 4.3 Run App

```bash
# iOS Simulator
flutter run -d ios

# Android Emulator
flutter run -d android

# Or list devices
flutter devices
```

✅ Client app running on simulator/emulator

## Step 5: Nutritionist Panel

### 5.1 Install Dependencies

```bash
cd apps/nutritionist-panel
npm install
```

### 5.2 Configure Environment

```bash
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_SOCKET_URL=http://localhost:3001" >> .env.local
```

### 5.3 Start Dev Server

```bash
npm run dev
```

✅ Nutritionist panel running at: http://localhost:3000

## Step 6: Admin Panel

### 6.1 Install Dependencies

```bash
cd apps/admin-panel
npm install
```

### 6.2 Configure Environment

```bash
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

### 6.3 Start Dev Server

```bash
npm run dev
```

✅ Admin panel running at: http://localhost:3002

## Step 7: Firebase Setup (Optional but Recommended)

### 7.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project: "GymGenius"
3. Enable Authentication (Email/Password, Google)
4. Enable Firestore Database
5. Enable Cloud Messaging

### 7.2 Download Service Account

1. Project Settings → Service Accounts
2. Generate new private key
3. Save as `firebase-service-account.json`
4. Place in `packages/backend/`

### 7.3 Configure Flutter Apps

1. iOS: Download `GoogleService-Info.plist` → `ios/Runner/`
2. Android: Download `google-services.json` → `android/app/`

### 7.4 Update Backend .env

```bash
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

## Quick Test

### Test Backend API

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"...","environment":"development"}
```

### Test Socket.io

Open browser console on http://localhost:3001 and run:

```javascript
const socket = io('http://localhost:3001', {
  auth: { token: 'test-token' },
});
socket.on('connect', () => console.log('Connected!'));
```

## Common Issues & Solutions

### Issue: PostgreSQL connection failed

**Solution:**

```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (macOS)
brew services start postgresql@15

# Create user if needed
createuser -s your_username
```

### Issue: Redis connection failed

**Solution:**

```bash
# Check if Redis is running
redis-cli ping

# Start Redis (macOS)
brew services start redis
```

### Issue: Flutter app can't connect to localhost

**Solution:** For Android emulator, use `10.0.2.2` instead of `localhost`:

```bash
API_BASE_URL=http://10.0.2.2:8000
```

For iOS simulator, `localhost` works fine.

### Issue: Poetry command not found

**Solution:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: Flutter not found

**Solution:**

```bash
# Download Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"
flutter doctor
```

## Development Workflow

### 1. Start all services:

```bash
# Terminal 1: Backend
cd packages/backend && poetry run uvicorn app.main:app --reload

# Terminal 2: Socket.io
cd packages/backend/socketio && npm run dev

# Terminal 3: Nutritionist Panel
cd apps/nutritionist-panel && npm run dev

# Terminal 4: Admin Panel
cd apps/admin-panel && npm run dev

# Terminal 5: Flutter Client App
cd apps/client-app && flutter run
```

### 2. Make changes and see live reload:

- Backend: Auto-reloads on file changes
- Socket.io: Auto-reloads via nodemon
- React panels: Hot module replacement
- Flutter: Hot reload with `r` key

### 3. Run tests:

```bash
# Backend tests
cd packages/backend
poetry run pytest

# Flutter tests
cd apps/client-app
flutter test

# React tests
cd apps/nutritionist-panel
npm test
```

## What's Next?

✅ **You're all set!** Your development environment is ready.

**Next steps:**

1. Review `docs/ARCHITECTURE.md` to understand the system
2. Check `docs/API.md` for API endpoints
3. Explore the codebase
4. Start implementing features!

## Need Help?

- **Architecture questions:** See `docs/ARCHITECTURE.md`
- **API reference:** See `docs/API.md`
- **Deployment:** See `docs/DEPLOYMENT.md`
- **Full implementation details:** See `IMPLEMENTATION_SUMMARY.md`

---

**Happy coding! 🚀**
