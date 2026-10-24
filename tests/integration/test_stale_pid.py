import json
import os

from supervisor.lock import (
    acquire_lock,
    process_start_time,
    read_lock,
    read_pid,
)


def test_stale_pid_replaced(tmp_path):
    path = tmp_path / "lock"
    path.write_text(
        json.dumps({"pid": 99999999, "start_time": "1"}),
        encoding="utf-8",
    )

    acquire_lock(path, pid=12345)

    assert read_pid(path) == 12345


def test_reused_pid_identity_is_replaced(tmp_path):
    path = tmp_path / "lock"
    current = os.getpid()

    path.write_text(
        json.dumps({
            "pid": current,
            "start_time": "definitely-not-the-current-process",
        }) + "\n",
        encoding="utf-8",
    )

    acquire_lock(path, pid=12345)

    record = read_lock(path)

    assert record is not None
    assert record["pid"] == 12345


def test_matching_pid_identity_is_live(tmp_path):
    path = tmp_path / "lock"
    current = os.getpid()

    path.write_text(
        json.dumps({
            "pid": current,
            "start_time": process_start_time(current),
        }) + "\n",
        encoding="utf-8",
    )

    record = read_lock(path)

    assert record is not None
    assert record["pid"] == current
