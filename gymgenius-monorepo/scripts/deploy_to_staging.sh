#!/bin/bash
set -euo pipefail

if [ -z "${STAGING_HOST:-}" ]; then
  echo "STAGING_HOST not set"
  exit 1
fi

if [ -z "${STAGING_SSH_KEY:-}" ]; then
  echo "STAGING_SSH_KEY not set"
  exit 1
fi

# This script is a minimal example that syncs the admin build to a staging host.
# Customize this for your environment. It assumes the `apps/admin-panel/.next` directory exists.

mkdir -p ~/.ssh
echo "$STAGING_SSH_KEY" > /tmp/staging_ssh_key
chmod 600 /tmp/staging_ssh_key

echo "Syncing admin build to ${STAGING_HOST}:/var/www/admin"
rsync -avz -e "ssh -i /tmp/staging_ssh_key -o StrictHostKeyChecking=no" apps/admin-panel/.next/ ubuntu@${STAGING_HOST}:/var/www/admin

rm /tmp/staging_ssh_key

echo "Staging deploy complete"
