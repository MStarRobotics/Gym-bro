# GymGenius Monorepo

![GymGenius CI/CD](https://github.com/<your-org>/<your-repo>/actions/workflows/ci.yml/badge.svg?branch=main)

Complete fitness ecosystem with AI-powered coaching, real-time communication,
and seamless payments.

## Architecture

### Packages

- **Backend** (FastAPI + PostgreSQL + Socket.io): Core API and real-time server

### Branch protection helper

You can mark the following checks as required for `main`/`develop`/`staging`
branch protection via the repo settings or using the helper script
`scripts/set-branch-protection.sh`.

Typical check names to add as required:

- `pre-commit-check`
- `admin-node-lint-check`
- `nutritionist-node-lint-check`
- `client-flutter-lint-check`
- `trainer-flutter-lint-check`
- `backend-tests`
- `legacy-backend-tests`

Required checks example:

- `pre-commit-check`
- `admin-node-lint-check`
- `nutritionist-node-lint-check`
- `client-flutter-lint-check`
- `trainer-flutter-lint-check`
- `backend-tests`
- `legacy-backend-tests`

Example using `gh` or `GH_ADMIN_TOKEN` (recommended):

```bash
GH_ADMIN_TOKEN=ghp_xxx \
  ./scripts/set-branch-protection.sh your-org your-repo main pre-commit-check admin-node-lint-check nutritionist-node-lint-check backend-tests
```

Note: The `scripts/set-branch-protection.sh` script requires an admin-level
token (GITHUB_TOKEN or GH_TOKEN) and will PATCH the repo's branch protection
rules using GitHub API.

Or use the GitHub Actions `workflow_dispatch` in
`.github/workflows/branch-protection.yml` by supplying inputs and the
`GH_ADMIN_TOKEN` secret under the repository Secrets. This workflow runs the
same helper script and can be executed manually via the GitHub Actions UI.

### CI Secrets for Android signing & staging S3

If you'd like CI to sign Android AAB/APKs and upload them to S3/staging server,
add these secrets to your repository:

- `ANDROID_KEYSTORE_BASE64` – base64-encoded Android keystore (decode in CI for
  signing)
- `ANDROID_KEYSTORE_PASSWORD` – password for the keystore
- `ANDROID_KEY_PASSWORD` – password for the key alias
- `ANDROID_KEY_ALIAS` – key alias
- `STAGING_AWS_ACCESS_KEY_ID` – AWS credentials for S3 upload in staging
  workflow
- `STAGING_AWS_SECRET_ACCESS_KEY` – AWS secret key
- `AWS_REGION` – AWS region (e.g. us-east-1)
- `STAGING_S3_BUCKET` – bucket to upload APK/AAB artifacts
- `STAGING_SSH_KEY` – ASCII-encoded private key for scp to staging host
- `STAGING_HOST` – staging server host to scp artifacts to (optional)
- `STAGING_DEPLOY` – set to `true` to allow deploy step to run

Store these in `Settings -> Secrets -> Actions` on GitHub. The `ci.yml` pipeline
will only perform signing and upload steps on `staging` branch or tags to avoid
exposing secrets in PR builds.

Additional GPlay / fastlane CI secrets:

- `GPLAY_SERVICE_ACCOUNT_JSON` – base64 encoded JSON key for Google Play service
  account
- `GPLAY_PACKAGE_NAME` – package name used to identify the Play Console app

Run a secrets presence check (manual trigger):

1. Go to the Actions tab.
2. Choose the `Secrets Presence Check` workflow.
3. Click `Run workflow` to check whether required secrets are present.

This workflow validates that signing keys and Play Store service account are
present and returns a non-zero exit code if any required secrets are missing.

- **Shared UI**: Reusable React components
- **Shared Types**: TypeScript type definitions

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, PostgreSQL, Socket.io, Redis
- **Mobile**: Flutter 3.16+, Provider, Firebase
- **Web**: Next.js 14, React 18, Tailwind CSS
- **Payments**: Razorpay (PhonePe/Google Pay)
- **Real-time**: Socket.io + Firestore hybrid
- **Auth**: Firebase Authentication
- **CI/CD**: GitHub Actions with path filters

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Flutter 3.16+
- PostgreSQL 15+
- Redis 7+

### Development Setup

1. **Backend**

```bash
cd packages/backend
poetry install
poetry run alembic upgrade head
```

### Dev Container

We provide a VS Code Dev Container configuration that includes tools for Python
development (Poetry, Black, Ruff) and Node to help develop the frontend.

Steps to use the devcontainer:

1. Open the repository in VS Code.
2. If prompted, Reopen the folder in a Container.
3. After the container builds, run `poetry install` inside the devcontainer
   workspace (or use the `Poetry Install (Backend)` task in VS Code Tasks).

This will ensure your editor has a consistent runtime and avoid missing import
diagnostics from Pylance/pyright.

Note: The devcontainer includes the Flutter SDK for tooling and development.
However it does **not** include Android SDK (or Xcode) — you will still need to
install the Android SDK and required platform tools to run or build Android
artifacts inside the devcontainer or on your host.

### Pre-commit & Linting

We use `pre-commit` to run formatters and linters: `black`, `ruff`, and `isort`.
Install `pre-commit` and run the hooks locally:

```bash
cd gymgenius-monorepo
pipx install pre-commit || pip install pre-commit
pre-commit install
pre-commit run --all-files
```

VS Code project tasks include common tasks such as `Backend Tests`,
`Lint (ruff)`.

Editor configuration & Dev Notes:

- Use the project's Poetry virtual environment for proper import resolution in
  your editor (VSCode/Pylance):
  1. Run `poetry env use python3.11` to create the venv.
  2. Run `poetry install` to install dependencies.
  3. In VSCode, set Python interpreter to the Poetry venv path (typically
     `~/.cache/pypoetry/virtualenvs/gymgenius-backend-<hash>/bin/python`).
  4. Restart your editor; missing stub warnings (e.g., SQLAlchemy, FastAPI)
     should disappear once the venv is selected.

Local test helper:

This repo has a `Makefile` with a convenient `make local-test` target that sets
up a sqlite test DB and runs backend tests. Use it for quick local validation:

```bash
make local-test
```

1. **Socket.io Server**

```bash
## Admin Panel (Next.js): System administration interface
- Default Dev Port: 3002
npm install
npm run dev:socketio
```

1. **Flutter Apps**

```bash
# Client App
cd apps/client-app
flutter pub get
flutter run

# Trainer App
cd apps/trainer-app
flutter pub get
flutter run
```

1. **React Panels**

```bash
# Nutritionist Panel
cd apps/nutritionist-panel
npm install
npm run dev

# Admin Panel
cd apps/admin-panel
npm install
npm run dev
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:pass@localhost:5432/gymgenius
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
RAZORPAY_KEY_ID=rzp_...
RAZORPAY_KEY_SECRET=...
FIREBASE_SERVICE_ACCOUNT=./firebase-service-account.json
```

### Flutter Apps (.env)

```
API_BASE_URL=http://localhost:8000
SOCKET_URL=http://localhost:3001
FIREBASE_CONFIG=...
```

## Deployment

See [docs/deployment.md](./docs/deployment.md) for production deployment guides.

## Contributing

See [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) for development guidelines.

## License

Proprietary - All rights reserved

## CI and Secrets (Quick Guide)

This repository's GitHub Actions workflows use CI-friendly local service
defaults so tests and builds run without forcing secrets into CI during PRs and
dev workflows.

CI defaults used in workflows (safe for CI and dev):

- PostgreSQL:
  - `POSTGRES_USER` = `postgres`
  - `POSTGRES_PASSWORD` = `postgres`
  - `POSTGRES_DB` = `gymgenius_test`

- Database connection string:
  - `DATABASE_URL` =
    `postgresql://postgres:postgres@localhost:5432/gymgenius_test`

- Redis:
  - `REDIS_URL` = `redis://localhost:6379/0`

Overriding in production (recommended):

1. Set the real secrets in GitHub (Repository > Settings > Secrets and
   variables > Actions):
   - `DATABASE_URL`, `REDIS_URL`, and any third-party keys (`OPENAI_API_KEY`,
     `GOOGLE_API_KEY`, `RAZORPAY_*`, etc.)
2. Update environment configuration in your deployment service (Heroku, GCP,
   AWS, Vercel, etc.) to use values stored securely as environment variables.
3. Make sure `SECRETS_CONFIGURATION.md` documents which keys are required for
   production and their intended usage.

Notes:

- Local CI defaults are only used for test automation and development scenarios;
  they should NOT be used in production.
- If your production environment uses hosted DB/Redis services, update your
  `DATABASE_URL` and `REDIS_URL` secrets accordingly.

CI Artifacts & QA Builds (Pull Requests):

- PRs that touch mobile apps will run QA debug builds and upload artifacts so QA
  team members can download test APKs directly from the GitHub Actions run.
  Artifacts include:
  - `client-qa-apk-<flavor>` — debug APK for client flavors (dev, qa, staging,
    prod)
  - `trainer-qa-apk-<flavor>` — debug APK for trainer flavors

These artifacts are unsigned debug APKs suitable for QA installation.

Emulator QA Test Harness:

- We added an `emulator-qa-test` job in `ci.yml` to run a headless Android
  emulator using the ReactiveCircus action and install built debug APKs for
  `client-app` and `trainer-app`. This helps verify APKs are installable and
  runnable in a CI environment without the physical device.

Secrets helper scripts: Nightly staging / pre-release deploy

- We added a nightly `staging-deploy` run (cron 02:00 UTC) and a `push` trigger
  on `main` so you can run a pre-release staging deploy automatically. This
  workflow still prefers artifacts produced by the `ci` workflow but will
  rebuild missing artifacts if necessary.

Fastlane internal track validation

- The `release.yml` now performs a `fastlane` validate/dry-run upload to the
  internal track (alpha) to validate AABs and verify the Play Console metadata
  is valid before the final production upload.

- `scripts/generate-keystore-base64.sh` — base64 encode a JKS keystore
- `scripts/ensure-secrets.sh` — list missing secrets and print `gh` CLI
  `gh secret set` commands to help set required repo secrets for staging and
  Play Console `fastlane` release automation.

Usage for secret helpers (from your terminal):

```bash
# Ensure gh is installed and logged in with an account that can manage repo
# secrets:
gh auth login
./scripts/ensure-secrets.sh your-org/your-repo
```

To set a keystore secret:

```bash
./scripts/generate-keystore-base64.sh path/to/key.jks | gh secret set ANDROID_KEYSTORE_BASE64 -R your-org/your-repo
gh secret set ANDROID_KEYSTORE_PASSWORD -R your-org/your-repo --body-file - <<EOF
<keystore-password>
EOF
```

Running integration tests (locally)

You can run the integration tests locally with a connected device/emulator. For
example:

```bash
cd apps/client-app
flutter pub get
flutter drive --driver=test_driver/integration_test_driver.dart --target=integration_test/app_test.dart
```

The emulator QA job runs the `flutter drive` instrumentation test inside the
`reactivecircus/android-emulator-runner` step on GitHub Actions so tests run in
a CI-provided emulator.

Branch protection & `GH_ADMIN_TOKEN`

If you want the `scripts/set-branch-protection.sh` automation to run, create a
`GH_ADMIN_TOKEN` secret with a personal access token that has repository admin
privileges. Use `./scripts/ensure-secrets.sh your-org/your-repo` to show the
`gh` CLI commands for setting secrets.
