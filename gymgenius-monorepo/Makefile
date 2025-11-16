SHELL := /bin/bash

.PHONY: help backend socketio nutritionist admin client trainer up down logs

help:
	@echo "GymGenius make targets"
	@echo "  make up          - Start backend + socketio + postgres + redis via docker-compose"
	@echo "  make backend     - Start backend (python + uvicorn) using Poetry"
	@echo "  make socketio    - Start Socket.io server"
	@echo "  make nutritionist - Start Next.js nutritionist panel"
	@echo "  make admin        - Start Next.js admin panel"

up:
	@docker compose -f docker-compose.dev.yml up -d --build

down:
	@docker compose -f docker-compose.dev.yml down

logs:
	@docker compose logs -f

backend:
	@cd packages/backend && poetry install || true
	@cd packages/backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

socketio:
	@cd packages/backend/socketio && npm install || true
	@cd packages/backend/socketio && npm run dev

nutritionist:
	@cd apps/nutritionist-panel && npm install || true
	@cd apps/nutritionist-panel && npm run dev

admin:
	@cd apps/admin-panel && npm install || true
	@cd apps/admin-panel && npm run dev

client:
	@cd apps/client-app && flutter pub get || true
	@cd apps/client-app && flutter run

trainer:
	@cd apps/trainer-app && flutter pub get || true
	@cd apps/trainer-app && flutter run

local-test:
	@cd packages/backend && poetry install --no-root || true
	@cd packages/backend && export DATABASE_URL=sqlite+aiosqlite:////tmp/gymgenius_dev.db && \
	  export REDIS_URL=redis://localhost:6379/0 && \
	  export SECRET_KEY=test-secret && \
	  export RAZORPAY_KEY_ID=rzp_test && \
	  export RAZORPAY_KEY_SECRET=test-secret && \
	  export FIREBASE_SERVICE_ACCOUNT_PATH=/tmp/gymgenius-firebase.json && \
	  echo '{}' > /tmp/gymgenius-firebase.json && \
	  PYTHONPATH=$(pwd) poetry run pytest -q
