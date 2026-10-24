from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from core.errors import StateError


LOCK_MODE = 0o600


def pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False

    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def process_start_time(pid: int) -> str | None:
    if pid <= 0:
        return None

    try:
        content = Path(f"/proc/{pid}/stat").read_text(
            encoding="utf-8",
        )
    except (FileNotFoundError, PermissionError, OSError):
        return None

    closing = content.rfind(")")

    if closing < 0:
        return None

    fields = content[closing + 2:].split()

    # Linux /proc/<pid>/stat field 22 is process start time.
    # After removing fields 1 and 2, it is index 19.
    if len(fields) <= 19:
        return None

    return fields[19]


def read_lock(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        pid = int(payload["pid"])
    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        TypeError,
    ):
        return None

    start_time = payload.get("start_time")

    return {
        "pid": pid,
        "start_time": (
            str(start_time)
            if start_time is not None
            else None
        ),
    }


def read_pid(path: Path) -> int | None:
    record = read_lock(path)

    if record is None:
        return None

    return int(record["pid"])


def lock_owner_alive(record: dict[str, Any]) -> bool:
    pid = int(record["pid"])

    if not pid_alive(pid):
        return False

    recorded_start = record.get("start_time")

    # Protect legacy PID-only locks conservatively.
    if recorded_start is None:
        return True

    actual_start = process_start_time(pid)

    # If process identity cannot be inspected, do not steal the lock.
    if actual_start is None:
        return True

    return str(recorded_start) == actual_start


def _record_for_pid(pid: int) -> dict[str, Any]:
    return {
        "pid": pid,
        "start_time": process_start_time(pid),
    }


def _write_exclusive(
    path: Path,
    record: dict[str, Any],
) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, LOCK_MODE)

    try:
        payload = (
            json.dumps(
                record,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )

        with os.fdopen(
            descriptor,
            "w",
            encoding="utf-8",
        ) as handle:
            descriptor = -1
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        if descriptor >= 0:
            os.close(descriptor)

    os.chmod(path, LOCK_MODE)


def acquire_lock(
    path: Path,
    pid: int | None = None,
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    owner = os.getpid() if pid is None else int(pid)

    for _ in range(3):
        try:
            _write_exclusive(path, _record_for_pid(owner))
            return owner
        except FileExistsError:
            existing = read_lock(path)

            if (
                existing is not None
                and lock_owner_alive(existing)
            ):
                raise StateError(
                    "daemon already running",
                    code="ERR_DAEMON_RUNNING",
                )

            try:
                path.unlink()
            except FileNotFoundError:
                pass

    raise StateError(
        "failed to acquire daemon lock",
        code="ERR_DAEMON_LOCK",
    )


def release_lock(
    path: Path,
    pid: int | None = None,
) -> None:
    expected = os.getpid() if pid is None else int(pid)
    record = read_lock(path)

    if (
        record is not None
        and int(record["pid"]) == expected
    ):
        path.unlink(missing_ok=True)
