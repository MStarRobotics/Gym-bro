# Staging deploy secrets

STAGING_DEPLOY: Set to `true` to enable automated staging deploys from the
`staging` branch.

STAGING_HOST: The hostname or IP address of the staging server that will receive
builds. (e.g., `staging.example.com`).

STAGING_SSH_KEY: Private SSH key for CI to authenticate with `STAGING_HOST`.
Only set this as a GitHub repository secret in the UI.

Important: The staging job will only run deployments if `STAGING_DEPLOY` is
`true` and `STAGING_SSH_KEY` and `STAGING_HOST` are defined as secrets.

<!-- markdownlint-configure-file {"MD022": false, "MD031": false, "MD032": false} -->

## GitHub Repository Secrets Configuration Guide

This document lists all secrets that need to be configured in your GitHub
repository for CI/CD pipelines to work correctly.

## How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret listed below

## Required Secrets

### Database Configuration

```
DATABASE_URL
```

**Value:** `postgresql://user:password@localhost:5432/gymgenius_test`
**Description:** PostgreSQL connection string for test database

```
POSTGRES_USER
```

**Value:** `gymgenius` **Description:** PostgreSQL username

```
POSTGRES_PASSWORD
```

**Value:** Your secure PostgreSQL password **Description:** PostgreSQL password

```
POSTGRES_DB
```

**Value:** `gymgenius_test` **Description:** PostgreSQL database name for tests

### Redis Configuration

```
REDIS_URL
```

**Value:** `redis://localhost:6379/0` **Description:** Redis connection string

### Payment Gateway

```
RAZORPAY_KEY_ID
```

**Value:** `rzp_test_XXXXXXXXXXXX` **Description:** Razorpay API Key ID (test or
live)

```
RAZORPAY_KEY_SECRET
```

**Value:** Your Razorpay secret key **Description:** Razorpay API Secret Key

### Authentication

```
JWT_SECRET_KEY
```

**Value:** A random 32+ character string **Description:** Secret key for JWT
token signing **Generation:** `openssl rand -hex 32`

### AI Services

```
GOOGLE_GEMINI_API_KEY
```

**Value:** Your Google Gemini API key **Description:** API key for Google Gemini
AI integration

```
OPENAI_API_KEY
```

**Value:** Your OpenAI API key (optional) **Description:** API key for OpenAI
GPT models

## Optional Secrets

### Code Coverage

```
CODECOV_TOKEN
```

**Value:** Your Codecov token **Description:** Token for uploading code coverage
reports

### Monitoring

```
SENTRY_DSN
```

**Value:** Your Sentry DSN **Description:** Sentry error tracking integration

## Validation

After adding secrets, the CI/CD workflow will validate that required secrets are
present before running tests. If a secret is missing, the workflow will fail
with a clear error message.

## Security Best Practices

1. **Never commit secrets to version control**
2. **Use different secrets for development, staging, and production**
3. **Rotate secrets regularly** (every 90 days recommended)
4. **Use test/sandbox credentials** for CI/CD pipelines
5. **Limit secret access** to necessary team members only

## Local Development

For local development, copy `.env.example` to `.env` and fill in your values:

```bash
# In gymgenius-monorepo/
cp .env.example .env

# In gymgenius/backend/
cp .env.example .env
```

## Troubleshooting

If CI/CD fails with "secret is not set" errors:

1. Verify the secret name matches exactly (case-sensitive)
2. Check that the secret has a non-empty value
3. Ensure the workflow has access to the secrets (check branch protection rules)
4. Re-run the workflow after adding missing secrets
