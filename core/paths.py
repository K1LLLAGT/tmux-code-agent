"""Path construction and safety invariants for M1 sessions."""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from core.errors import PathSafetyError
from core.ids import display_session_id, validate_session_id

PRIVATE_DIR_MODE: Final[int] = 0o700
STATE_ROOT_PARTS: Final[tuple[str, ...]] = (".local", "state", "tmux-code-agent", "sessions")
RUNTIME_PREFIX: Final[str] = "tca-"
UNIX_PATH_LIMIT: Final[int] = 107


@dataclass(frozen=True, slots=True)
class SessionPaths:
    """Durable and short-lived paths belonging to one session."""

    session_id: str
    state_root: Path
    state_dir: Path
    runtime_root: Path
    runtime_dir: Path

    @property
    def manifest(self) -> Path:
        return self.state_dir / "manifest.json"

    @property
    def state(self) -> Path:
        return self.state_dir / "state.json"

    @property
    def tmux_socket(self) -> Path:
        return self.runtime_dir / "tmux.sock"

    @property
    def control_socket(self) -> Path:
        return self.runtime_dir / "ctl.sock"


def default_state_root(home: str | os.PathLike[str]) -> Path:
    return Path(home).expanduser().joinpath(*STATE_ROOT_PARTS)


def default_runtime_root(prefix: str | os.PathLike[str]) -> Path:
    return Path(prefix).expanduser() / "tmp"


def build_session_paths(
    session_id: object,
    *,
    home: str | os.PathLike[str],
    prefix: str | os.PathLike[str],
) -> SessionPaths:
    canonical = validate_session_id(session_id)
    state_root = default_state_root(home)
    runtime_root = default_runtime_root(prefix)
    paths = SessionPaths(
        session_id=canonical,
        state_root=state_root,
        state_dir=state_root / canonical,
        runtime_root=runtime_root,
        runtime_dir=runtime_root / f"{RUNTIME_PREFIX}{display_session_id(canonical)}",
    )
    assert_unix_path(paths.tmux_socket)
    assert_unix_path(paths.control_socket)
    return paths


def ensure_private_dir(path: str | os.PathLike[str]) -> Path:
    """Create/repair a private directory and reject non-directories."""

    target = Path(path)
    try:
        target.mkdir(mode=PRIVATE_DIR_MODE, parents=True, exist_ok=True)
    except OSError as exc:
        raise PathSafetyError(
            f"cannot create private directory: {target}",
            code="ERR_PRIVATE_DIR",
        ) from exc
    if target.is_symlink() or not target.is_dir():
        raise PathSafetyError(
            f"private path is not a real directory: {target}",
            code="ERR_PRIVATE_DIR",
        )
    try:
        target.chmod(PRIVATE_DIR_MODE)
    except OSError as exc:
        raise PathSafetyError(
            f"cannot secure private directory: {target}",
            code="ERR_PRIVATE_DIR",
        ) from exc
    mode = stat.S_IMODE(target.stat().st_mode)
    if mode != PRIVATE_DIR_MODE:
        raise PathSafetyError(
            f"private directory mode is not 0700: {target}",
            code="ERR_PRIVATE_DIR_MODE",
        )
    return target


def create_session_dirs(paths: SessionPaths) -> SessionPaths:
    """Create private session dirs without chmod'ing the shared runtime root."""

    old_umask = os.umask(0o077)
    try:
        ensure_private_dir(paths.state_root)
        ensure_private_dir(paths.state_dir)
        try:
            paths.runtime_root.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise PathSafetyError(
                f"cannot create runtime root: {paths.runtime_root}",
                code="ERR_RUNTIME_ROOT",
            ) from exc
        if paths.runtime_root.is_symlink() or not paths.runtime_root.is_dir():
            raise PathSafetyError(
                f"runtime root is not a real directory: {paths.runtime_root}",
                code="ERR_RUNTIME_ROOT",
            )
        ensure_private_dir(paths.runtime_dir)
    finally:
        os.umask(old_umask)
    return paths


def assert_unix_path(path: str | os.PathLike[str], limit: int = UNIX_PATH_LIMIT) -> Path:
    """Reject encoded Unix-socket paths that exceed the conservative limit."""

    target = Path(path)
    length = len(os.fsencode(target))
    if length > limit:
        raise PathSafetyError(
            f"Unix socket path is too long ({length}>{limit}): {target}",
            code="ERR_UNIX_PATH_TOO_LONG",
        )
    return target


def validate_workspace(
    workspace: str | os.PathLike[str],
    *,
    home: str | os.PathLike[str],
    allow_home: bool = False,
    allow_root: bool = False,
) -> Path:
    """Resolve a launch workspace and enforce the M1 HOME/root guard."""

    candidate = Path(workspace).expanduser()
    try:
        resolved = candidate.resolve(strict=True)
        home_resolved = Path(home).expanduser().resolve(strict=True)
    except OSError as exc:
        raise PathSafetyError(
            f"workspace or home cannot be resolved: {candidate}",
            code="ERR_WORKSPACE_RESOLVE",
        ) from exc
    if not resolved.is_dir():
        raise PathSafetyError(
            f"workspace is not a directory: {resolved}",
            code="ERR_WORKSPACE_NOT_DIR",
        )
    if resolved == Path(resolved.anchor) and not allow_root:
        raise PathSafetyError(
            "refusing to use filesystem root as workspace without explicit override",
            code="ERR_WORKSPACE_ROOT",
        )
    if resolved == home_resolved and not allow_home:
        raise PathSafetyError(
            "refusing to use HOME as workspace without explicit override",
            code="ERR_WORKSPACE_HOME",
        )
    return resolved
