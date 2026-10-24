"""Immutable launch manifest schema and exclusive writer."""

from __future__ import annotations

import json
import os
import stat
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.context import InvocationContext
from core.errors import StateError
from core.paths import SessionPaths

MANIFEST_SCHEMA_VERSION = 1
MANIFEST_MODE = 0o400


@dataclass(frozen=True, slots=True)
class LaunchManifest:
    schema_version: int
    session_id: str
    created_at: str
    workspace: str
    home: str
    prefix: str
    shell: str | None
    term: str | None
    context: dict[str, Any]
    state_dir: str
    runtime_dir: str
    tmux_socket: str
    control_socket: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_manifest(context: InvocationContext, paths: SessionPaths) -> LaunchManifest:
    return LaunchManifest(
        schema_version=MANIFEST_SCHEMA_VERSION,
        session_id=paths.session_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        workspace=context.workspace,
        home=context.home,
        prefix=context.prefix,
        shell=context.shell,
        term=context.term,
        context=context.as_dict(),
        state_dir=str(paths.state_dir),
        runtime_dir=str(paths.runtime_dir),
        tmux_socket=str(paths.tmux_socket),
        control_socket=str(paths.control_socket),
    )


def write_manifest(path: Path, manifest: LaunchManifest) -> Path:
    payload = json.dumps(manifest.as_dict(), indent=2, sort_keys=True) + "\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(path, MANIFEST_MODE)
    except FileExistsError as exc:
        raise StateError("manifest already exists", code="ERR_MANIFEST_EXISTS") from exc
    except OSError as exc:
        raise StateError("manifest write failed", code="ERR_MANIFEST_WRITE") from exc
    if stat.S_IMODE(path.stat().st_mode) != MANIFEST_MODE:
        raise StateError("manifest mode is not 0400", code="ERR_MANIFEST_MODE")
    return path
