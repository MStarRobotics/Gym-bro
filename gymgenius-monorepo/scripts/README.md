# Scripts for GymGenius repo

## set-branch-protection.sh

This script sets branch protection rules on a GitHub repository's branch via the
GitHub API.

Usage:

```bash
GH_TOKEN=... ./scripts/set-branch-protection.sh [--dry-run] <owner> <repo> <branches> <context1> [<context2> ...]
```

Examples:

```bash
GH_TOKEN=... ./scripts/set-branch-protection.sh my-org my-repo "main,release" "github-actions/ci"
GH_TOKEN=... ./scripts/set-branch-protection.sh -n my-org my-repo "main" "github-actions/ci sonar"
```

The script supports comma-separated or space-separated lists of branches and
contexts. Use the `--dry-run` or `-n` option to print the JSON payload instead
of calling GitHub.
