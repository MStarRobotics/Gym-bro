import json
import os
import subprocess


def run_dry_run_and_extract_payload(owner, repo, branches, contexts):
    script = os.path.join(os.getcwd(), "scripts", "set-branch-protection.sh")
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = "fake"
    cmd = ["bash", script, "--dry-run", owner, repo, branches, contexts]
    out = subprocess.check_output(
        cmd, env=env, stderr=subprocess.STDOUT, text=True
    )
    # payload JSON is printed by the script in dry-run mode - extract the
    # JSON object
    # The script prints the payload for every branch. Find a single top-level
    # JSON object by scanning from the first '{' and finding the matching
    # closing '}' accounting for nested braces.
    start = out.find("{")
    if start == -1:
        raise AssertionError("No JSON payload found in output")
    depth = 0
    end = None
    for i in range(start, len(out)):
        c = out[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise AssertionError("Did not find end of JSON payload")
    payload_str = out[start:end]
    # Parse JSON
    payload = json.loads(payload_str)
    return payload


def test_payload_has_required_fields_and_contexts():
    owner = "my-org"
    repo = "my-repo"
    branches = "main,release"
    contexts = "github-actions/ci,sonar"
    payload = run_dry_run_and_extract_payload(owner, repo, branches, contexts)
    assert "required_status_checks" in payload
    r = payload["required_status_checks"]
    assert r.get("strict") is True
    assert "contexts" in r
    assert set(r["contexts"]) == {"github-actions/ci", "sonar"}
    assert payload.get("enforce_admins") is True
    assert "required_pull_request_reviews" in payload
