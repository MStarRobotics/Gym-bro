# Developer Setup & Local Test Run (GymGenius)

This file contains recommended steps to set up the development environment and
run frontend/backend tests locally.

## Prerequisites

- Node.js 20.x (NVM recommended)
- Python 3.11 (pyenv recommended)
- Docker (for backend Postgres & Redis local testing)
- Yarn or npm (we use npm in scripts)

## Frontend (Root Vite App)

```bash
# Install dependencies
npm ci

# Run dev server
npm run dev

# Run vitest
npm run test

# Run strict lint locally (will fail on issues)
npm run lint:strict
```

## Next.js Admin & Nutritionist Panel (monorepo)

```bash
cd gymgenius-monorepo/apps/admin-panel
npm ci
npm run dev
npm run lint
npm run type-check
npm run build
```

```bash
cd gymgenius-monorepo/apps/nutritionist-panel
npm ci
npm run dev
npm run lint
npm run type-check
npm run build
```

## Backend (Poetry) — Local Dev with Docker Compose

```bash
# Start DB & Redis
cd gymgenius-monorepo
docker compose -f docker-compose.dev.yml up -d

# Set test env vars
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/gymgenius_test"
export REDIS_URL="redis://localhost:6379/0"

# Run backend tests
cd packages/backend
poetry install
poetry run pytest --cov=app --cov-report=term-missing
```

## Dev Tooling

- Investigate tools mismatch: `npm run audit-devtools` (fail on mismatches)
- Sync dev tools with the approved matrix: `npm run sync-devtools:apply`
  (updates package.json)
- Report React versions: `npm run report-react-versions` (exits non-zero if
  mismatched)

## Notes & Tips

- The repo purposely uses the `dev_tool_versions.json` mapping to keep a single
  source of truth for dev/test tools; run `npm run sync-devtools` with `--apply`
  to apply the mapping across workspaces.
- The CI `dev-tools-audit` job will fail on mismatches; fix them locally via
  `npm run sync-devtools:apply`.
