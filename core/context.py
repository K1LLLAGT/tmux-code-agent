"""Immutable invocation-context and Git/project fact capture."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from core.errors import ContextError
from core.paths import validate_workspace
from redact.env import filter_environment


@dataclass(frozen=True, slots=True)
class GitFacts:
    is_repo: bool
    root: str | None = None
    branch: str | None = None
    head: str | None = None
    dirty: bool | None = None
    detached: bool | None = None
    bare: bool | None = None


@dataclass(frozen=True, slots=True)
class InvocationContext:
    logical_pwd: str
    physical_pwd: str
    workspace: str
    home: str
    prefix: str
    shell: str | None
    term: str | None
    locale: dict[str, str]
    environment: dict[str, str]
    python_executable: str
    python_version: str
    virtual_env: str | None
    node_env: str | None
    git: GitFacts

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _git(workspace: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }
    return subprocess.run(
        ["git", "-C", str(workspace), *args],
        text=True,
        capture_output=True,
        timeout=5,
        env=env,
        check=False,
    )


def capture_git_facts(workspace: Path) -> GitFacts:
    probe = _git(workspace, "rev-parse", "--is-inside-work-tree")
    bare_probe = _git(workspace, "rev-parse", "--is-bare-repository")
    inside = probe.returncode == 0 and probe.stdout.strip() == "true"
    bare = bare_probe.returncode == 0 and bare_probe.stdout.strip() == "true"
    if not inside and not bare:
        return GitFacts(is_repo=False)

    root_probe = _git(workspace, "rev-parse", "--show-toplevel")
    head_probe = _git(workspace, "rev-parse", "HEAD")
    branch_probe = _git(workspace, "symbolic-ref", "--quiet", "--short", "HEAD")
    status_probe = _git(workspace, "status", "--porcelain=v1", "--untracked-files=normal")
    branch = branch_probe.stdout.strip() if branch_probe.returncode == 0 else None
    return GitFacts(
        is_repo=True,
        root=root_probe.stdout.strip() if root_probe.returncode == 0 else str(workspace),
        branch=branch,
        head=head_probe.stdout.strip() if head_probe.returncode == 0 else None,
        dirty=bool(status_probe.stdout) if status_probe.returncode == 0 else None,
        detached=branch is None and head_probe.returncode == 0,
        bare=bare,
    )


def capture_context(
    *,
    logical_pwd: str | os.PathLike[str] | None = None,
    environ: dict[str, str] | None = None,
    allow_home: bool = False,
    allow_root: bool = False,
) -> InvocationContext:
    source = dict(os.environ if environ is None else environ)
    home = source.get("HOME")
    prefix = source.get("PREFIX")
    if not home or not prefix:
        raise ContextError("HOME and PREFIX are required", code="ERR_CONTEXT_ENV")

    logical = str(logical_pwd or source.get("PWD") or os.getcwd())
    workspace = validate_workspace(
        logical,
        home=home,
        allow_home=allow_home,
        allow_root=allow_root,
    )
    try:
        physical = Path(logical).expanduser().resolve(strict=True)
    except OSError as exc:
        raise ContextError("working directory cannot be resolved") from exc

    safe_env = filter_environment(source)
    locale = {
        key: value
        for key, value in safe_env.items()
        if key == "LANG" or key.startswith("LC_")
    }
    return InvocationContext(
        logical_pwd=logical,
        physical_pwd=str(physical),
        workspace=str(workspace),
        home=str(Path(home).expanduser().resolve()),
        prefix=str(Path(prefix).expanduser().resolve()),
        shell=source.get("SHELL"),
        term=source.get("TERM"),
        locale=locale,
        environment=safe_env,
        python_executable=sys.executable,
        python_version=".".join(map(str, sys.version_info[:3])),
        virtual_env=source.get("VIRTUAL_ENV") or source.get("CONDA_PREFIX"),
        node_env=source.get("NODE_ENV"),
        git=capture_git_facts(workspace),
    )
