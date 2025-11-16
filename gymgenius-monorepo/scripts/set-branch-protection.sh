#!/usr/bin/env bash
set -euo pipefail

# Usage: GH_TOKEN=... ./scripts/set-branch-protection.sh <owner> <repo> <branches> <context1> [<context2> ...]
# `branches` accepts a comma-separated or space-separated list of branches to set protection on.

DRY_RUN=false
if [ "${1:-}" = "--dry-run" ] || [ "${1:-}" = "-n" ]; then
  DRY_RUN=true
  shift
fi

if [ "$#" -lt 4 ]; then
  echo "Usage: GH_TOKEN=... $0 [--dry-run] <owner> <repo> <branches> <context1> [<context2> ...]" >&2
  echo "Example: GH_TOKEN=... $0 my-org my-repo 'main,release' github-actions/ci" >&2
  exit 2
fi

OWNER="$1"
REPO="$2"
BRANCHES="$3"
shift 3
CONTEXTS=("$@")

# Normalize branches: support comma-separated or space-separated list
oldIFS="$IFS"
IFS=',' read -r -a BRANCH_ARR <<< "$BRANCHES"
if [ ${#BRANCH_ARR[@]} -eq 1 ]; then
  # Try splitting by whitespace
  IFS=' ' read -r -a BRANCH_ARR <<< "${BRANCH_ARR[0]}"
fi
IFS="$oldIFS"

# Branch array ready: BRANCH_ARR[@]

# If a single argument is passed that contains spaces or commas, split into array
# If a single argument is passed that contains spaces or commas, split into array
if [ "${#CONTEXTS[@]}" -eq 1 ]; then
  CON_STR="${CONTEXTS[0]}"
  oldIFS="$IFS"
  if [[ "${CON_STR}" == *,* ]]; then
    IFS=',' read -r -a CONTEXTS <<< "${CON_STR}"
  else
    IFS=' ' read -r -a CONTEXTS <<< "${CON_STR}"
  fi
  IFS="$oldIFS"
fi

if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${GH_TOKEN:-}" ]; then
  echo "Error: GITHUB_TOKEN or GH_TOKEN must be set" >&2
  exit 1
fi

TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"

CONTEXTS_JSON=$(printf '"%s",' "${CONTEXTS[@]}" | sed 's/,$//')

PAYLOAD=$(cat <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": [${CONTEXTS_JSON}]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}
EOF
)

for branch in "${BRANCH_ARR[@]}"; do
  echo "Applying branch protection to ${OWNER}/${REPO} branch ${branch} with contexts: ${CONTEXTS[*]}"
  if [ "$DRY_RUN" = true ]; then
    echo "--- Dry run: would call GitHub API for branch: ${branch} ---"
    printf '%s\n' "${PAYLOAD}"
    continue
  fi

  # Call GitHub API and fail on HTTP status >= 400. Capture body for better error output.
  response=$(curl -sS --fail -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X PUT "https://api.github.com/repos/${OWNER}/${REPO}/branches/${branch}/protection" \
    -d "${PAYLOAD}" 2>&1) || {
    echo "Failed to apply branch protection to ${OWNER}/${REPO} branch ${branch}" >&2
    echo "curl output: ${response}" >&2
    exit 1
  }
  echo "Response: ${response}"
done

echo "Branch protection updated"
