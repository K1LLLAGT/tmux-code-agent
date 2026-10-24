import json
import os

import pytest

from core.errors import StateError
from supervisor.lock import (
    acquire_lock,
    process_start_time,
    read_lock,
    read_pid,
    release_lock,
)


def test_lock(tmp_path):
    path = tmp_path / "lock"

    acquire_lock(path)

    record = read_lock(path)

    assert record is not None
    assert record["pid"] == os.getpid()
    assert record["start_time"] == process_start_time(os.getpid())
    assert read_pid(path) == os.getpid()
    assert path.stat().st_mode & 0o777 == 0o600

    release_lock(path)

    assert not path.exists()


def test_live_lock_cannot_be_stolen(tmp_path):
    path = tmp_path / "lock"

    acquire_lock(path)

    with pytest.raises(StateError) as captured:
        acquire_lock(path, pid=12345)

    assert captured.value.code == "ERR_DAEMON_RUNNING"
    assert read_pid(path) == os.getpid()


def test_release_requires_matching_owner(tmp_path):
    path = tmp_path / "lock"

    acquire_lock(path)

    release_lock(path, pid=12345)

    assert path.exists()

    release_lock(path)

    assert not path.exists()


def test_legacy_live_pid_lock_is_protected(tmp_path):
    path = tmp_path / "lock"
    path.write_text(
        json.dumps({"pid": os.getpid()}) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(StateError):
        acquire_lock(path, pid=12345)
