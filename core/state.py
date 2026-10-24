"""Mutable session state schema and atomic file writer."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.errors import StateError

STATE_SCHEMA_VERSION = 1
STATE_MODE = 0o600


@dataclass(frozen=True, slots=True)
class SessionState:
    schema_version: int
    session_id: str
    status: str
    updated_at: str
    components: dict[str, str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def initial_state(session_id: str) -> SessionState:
    return SessionState(
        schema_version=STATE_SCHEMA_VERSION,
        session_id=session_id,
        status="CREATED",
        updated_at=datetime.now(timezone.utc).isoformat(),
        components={},
    )


def write_state_atomic(path: Path, state: SessionState) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state.as_dict(), indent=2, sort_keys=True) + "\n"
    temporary: str | None = None
    try:
        fd, temporary = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=path.parent)
        os.fchmod(fd, STATE_MODE)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        os.chmod(path, STATE_MODE)
    except OSError as exc:
        raise StateError("state write failed", code="ERR_STATE_WRITE") from exc
    finally:
        if temporary:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
    return path
