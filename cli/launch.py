"""M1 launch orchestration and dry-run creation path."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from core.config import Config
from core.context import capture_context
from core.ids import new_session_id
from core.manifest import build_manifest, write_manifest
from core.paths import SessionPaths, assert_unix_path, build_session_paths, create_session_dirs
from core.state import initial_state, write_state_atomic


def _override_paths(paths: SessionPaths, config: Config) -> SessionPaths:
    state_root = Path(config.state_root).expanduser() if config.state_root else paths.state_root
    runtime_root = Path(config.runtime_root).expanduser() if config.runtime_root else paths.runtime_root
    overridden = SessionPaths(
        session_id=paths.session_id,
        state_root=state_root,
        state_dir=state_root / paths.session_id,
        runtime_root=runtime_root,
        runtime_dir=runtime_root / paths.runtime_dir.name,
    )
    assert_unix_path(overridden.tmux_socket)
    assert_unix_path(overridden.control_socket)
    return overridden


def dry_run_start(
    *,
    workspace: str | None,
    config: Config,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    source = dict(os.environ if environ is None else environ)
    context = capture_context(
        logical_pwd=workspace,
        environ=source,
        allow_home=config.allow_home_workspace,
        allow_root=config.allow_root_workspace,
    )
    session_id = new_session_id()
    paths = build_session_paths(session_id, home=context.home, prefix=context.prefix)
    paths = _override_paths(paths, config)
    create_session_dirs(paths)
    manifest = build_manifest(context, paths)
    write_manifest(paths.manifest, manifest)
    state = initial_state(session_id)
    write_state_atomic(paths.state, state)
    return {
        "dry_run": True,
        "session_id": session_id,
        "context": context.as_dict(),
        "manifest": manifest.as_dict(),
        "state": state.as_dict(),
        "config": config.as_dict(),
        "paths": {
            "state_dir": str(paths.state_dir),
            "runtime_dir": str(paths.runtime_dir),
            "manifest": str(paths.manifest),
            "state": str(paths.state),
            "tmux_socket": str(paths.tmux_socket),
            "control_socket": str(paths.control_socket),
        },
    }
