#!/usr/bin/env bash
set -eu -o pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
BACKEND_DIR="$ROOT_DIR/gymgenius/backend"

cd "$BACKEND_DIR"

echo "Running backend CI checks..."
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  echo "Using Docker to run backend tests"
  if docker build --pull -t gymgenius-backend-test .; then
    echo "Docker image built; running container"
    if ! docker run --rm gymgenius-backend-test; then
      echo "Docker container reported failure; exiting"
      exit 1
    fi
  else
    echo "Docker build failed; falling back to local venv tests"
  fi
else
  echo "Docker not available or daemon not running; using Python venv for local tests"
  python3 -m venv .venv
  # shellcheck disable=SC1091
  . .venv/bin/activate
  python -m pip install --upgrade pip
  if ! pip install -r requirements.txt; then
    echo "Failed to install requirements in venv."
    echo "If this is due to psycopg2, install PostgreSQL build tools (e.g. 'brew install postgresql' on macOS or 'apt-get install libpq-dev' on Linux)."
    exit 1
  fi
  PYTHONPATH=. pytest -q
fi

echo "Backend CI checks done"
