#!/usr/bin/env bash
set -euo pipefail

echo "== GymGenius Environment Check =="

check() {
  CMD=$1
  DESC=$2
  if command -v "$CMD" >/dev/null 2>&1; then
    echo "[OK] $DESC -> $(command -v $CMD)"
  else
    echo "[MISSING] $DESC -> Please install $CMD"
  fi
}

check python "Python 3.11+ (python)"
check poetry "Poetry (poetry, recommended for backend)"
check node "Node.js (node)"
check npm "npm"
check docker "Docker"
check docker-compose "Docker Compose (docker-compose)"
check flutter "Flutter"

echo "\n== Versions (approx) =="
if command -v python >/dev/null 2>&1; then
  python --version || true
fi
if command -v node >/dev/null 2>&1; then
  node --version || true
fi
if command -v flutter >/dev/null 2>&1; then
  flutter --version || true
fi

echo "\n== Quick Notes =="
echo "- Ensure you set env variables (see .env.example files)."
echo "- For local development use docker-compose.dev.yml to run Postgres & Redis."
echo "- Use poetry to install backend dependencies: (cd packages/backend && poetry install)"

exit 0
