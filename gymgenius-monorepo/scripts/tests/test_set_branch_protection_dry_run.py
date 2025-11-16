import os
import subprocess


def run_dry_run(owner, repo, branches, contexts):
    script = os.path.join(os.getcwd(), "scripts", "set-branch-protection.sh")
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = "fake"
    cmd = ["bash", script, "--dry-run", owner, repo, branches, contexts]
    out = subprocess.check_output(
        cmd, env=env, stderr=subprocess.STDOUT, text=True
    )
    return out


def test_dry_run_includes_branches_and_contexts():
    owner = "my-org"
    repo = "my-repo"
    branches = "main,release"
    contexts = "github-actions/ci,sonar"  # comma-separated contexts

    out = run_dry_run(owner, repo, branches, contexts)
    # It should print the payload JSON and branch names
    assert "main" in out
    assert "release" in out
    assert "github-actions/ci" in out
    assert "sonar" in out


def test_error_when_no_token_and_no_dry_run():
    owner = "my-org"
    repo = "my-repo"
    branches = "main"
    contexts = "ci"
    script = os.path.join(os.getcwd(), "scripts", "set-branch-protection.sh")
    cmd = ["bash", script, owner, repo, branches, contexts]
    env = os.environ.copy()
    # ensure no token
    env.pop("GITHUB_TOKEN", None)
    env.pop("GH_TOKEN", None)
    try:
        subprocess.check_output(
            cmd, env=env, stderr=subprocess.STDOUT, text=True
        )
        assert False, "Expected script to exit due to missing token"
    except subprocess.CalledProcessError as e:
        assert e.returncode == 1
        assert "Error: GITHUB_TOKEN or GH_TOKEN must be set" in e.output


def test_space_separated_branches_and_contexts():
    owner = "my-org"
    repo = "my-repo"
    branches = "main release"
    contexts = "github-actions/ci sonar"  # space-separated contexts
    out = run_dry_run(owner, repo, branches, contexts)
    assert "main" in out
    assert "release" in out
    assert "github-actions/ci" in out
    assert "sonar" in out


def test_missing_args_exits_with_usage_code():
    script = os.path.join(os.getcwd(), "scripts", "set-branch-protection.sh")
    cmd = ["bash", script, "my-org", "my-repo"]  # only 2 args
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = "fake"
    try:
        subprocess.check_output(
            cmd, env=env, stderr=subprocess.STDOUT, text=True
        )
        assert False, "Expected script to exit due to missing args"
    except subprocess.CalledProcessError as e:
        assert e.returncode == 2
