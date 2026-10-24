import os
import subprocess
from pathlib import Path

from core.context import capture_context, capture_git_facts


def base_env(home: Path, prefix: Path, workspace: Path) -> dict[str, str]:
    return {
        "HOME": str(home),
        "PREFIX": str(prefix),
        "PWD": str(workspace),
        "PATH": os.environ["PATH"],
        "SHELL": "/bin/zsh",
        "TERM": "xterm-256color",
        "LANG": "en_US.UTF-8",
        "API_TOKEN": "never-persist",
    }


def test_capture_context_allowlists_environment(tmp_path: Path) -> None:
    home = tmp_path / "home"
    prefix = tmp_path / "prefix"
    workspace = home / "project"
    workspace.mkdir(parents=True)
    prefix.mkdir()
    context = capture_context(logical_pwd=workspace, environ=base_env(home, prefix, workspace))
    assert context.workspace == str(workspace.resolve())
    assert context.logical_pwd == str(workspace)
    assert "API_TOKEN" not in context.environment
    assert context.shell == "/bin/zsh"


def test_git_facts_clean_dirty_and_detached(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
    (repo / "a.txt").write_text("a")
    subprocess.run(["git", "-C", str(repo), "add", "a.txt"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True)
    clean = capture_git_facts(repo)
    assert clean.is_repo and clean.dirty is False and clean.head
    (repo / "a.txt").write_text("b")
    assert capture_git_facts(repo).dirty is True
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach", "-q"], check=True)
    assert capture_git_facts(repo).detached is True
