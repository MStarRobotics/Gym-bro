#!/usr/bin/env python3
"""
Check for occurrences of `--dart-define=TEST_MODE=true` in CI/workflow files
and fail if found outside allowed workflow files.

This script is used to protect release/deploy pipelines from including
`TEST_MODE`.
"""
import os
import sys

ALLOWED_WORKFLOWS = {
    "ci.yml",
    "nightly-integration.yml",
}

def find_violations(repo_root: str):
    path = os.path.join(repo_root, ".github", "workflows")
    violations = []
    if not os.path.isdir(path):
        return violations
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
        if "--dart-define=TEST_MODE=true" in content:
            # If file allowed, skip
            if fname in ALLOWED_WORKFLOWS:
                continue
            # count occurrences of the token
            cnt = content.count("--dart-define=TEST_MODE=true")
            violations.append((fname, cnt))
    return violations


def main():
    repo_root = os.getcwd()
    violations = find_violations(repo_root)
    if violations:
        print("Found TEST_MODE occurrences in disallowed workflow files:")
        for fname, cnt in violations:
            print(f" - {fname}: {cnt} occurrences")
        return 2
    print("No forbidden TEST_MODE occurrences detected.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
