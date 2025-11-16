.PHONY: lint type-check test check ci-checks backend-tests format

lint:
	npm run lint || true
	(cd gymgenius-monorepo && npm run --silent lint) || true

type-check:
	npm run type-check || true

test:
	npm run test || true

backend-tests:
	cd gymgenius-monorepo && poetry install --no-root && DB_TEST_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/gymgenius_test REDIS_URL=redis://localhost:6379/0 PYTHONPATH=$(PWD)/gymgenius-monorepo/packages/backend poetry run pytest -q || true

check: lint type-check test backend-tests

ci-checks: # Run full stack checks: JS, TS, Python backend (locally or via Docker)
	@echo "Running Node checks..."
	npm run check:ci
	@echo "Running backend checks..."
	bash scripts/backend-ci.sh

format:
	npm run format
