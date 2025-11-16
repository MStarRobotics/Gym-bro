#!/usr/bin/env bash
set -euo pipefail

REPO=${1:-}
if [[ -z "$REPO" ]]; then
  echo "Usage: $0 <owner/repo>"
  exit 1
fi

SECRETS=(
  ANDROID_KEYSTORE_BASE64
  ANDROID_KEYSTORE_PASSWORD
  ANDROID_KEY_PASSWORD
  ANDROID_KEY_ALIAS
  GPLAY_SERVICE_ACCOUNT_JSON
  GPLAY_PACKAGE_NAME
  STAGING_AWS_ACCESS_KEY_ID
  STAGING_AWS_SECRET_ACCESS_KEY
  STAGING_S3_BUCKET
  STAGING_SSH_KEY
  STAGING_HOST
  GH_ADMIN_TOKEN
)

echo "This helper will print gh CLI commands to set missing secrets in ${REPO}"
echo "Please ensure you have 'gh' CLI installed and authenticated with an account that can manage repository secrets."
echo
for s in "${SECRETS[@]}"; do
  if gh secret list -R "$REPO" | grep -q "^$s$"; then
    echo "SECRET OK: $s"
  else
    echo "SECRET MISSING: $s"
    echo "Use the following command to set it (example using an environment variable):"
    echo "  echo \"<value>\" | gh secret set $s -R $REPO"
    echo "Or to set from a file (for base64 json or keystore):"
    echo "  gh secret set $s --body-file /path/to/file -R $REPO"
    if [[ "$s" == "GH_ADMIN_TOKEN" ]]; then
      echo "If you want to automate branch protection, set GH_ADMIN_TOKEN via gh CLI:"
      echo "  gh secret set GH_ADMIN_TOKEN --body-file /path/to/token-file -R $REPO"
    fi
  fi
done
