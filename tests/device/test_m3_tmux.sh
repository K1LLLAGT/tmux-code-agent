#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}"
PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}"

cd "$ROOT"

rt="$PREFIX/tmp/tca-m3-dev-$$"
sock="$rt/tmux.sock"
work="$rt/work"

mkdir -p "$work"

cleanup() {
  tmux -S "$sock" kill-server 2>/dev/null || true
  rm -rf "$rt"
}

trap cleanup EXIT

SOCK="$sock" \
WORK="$work" \
"$PY" - <<'PY'
import os
import time
from pathlib import Path

from tmuxctl.control import ControlClient
from tmuxctl.panes import registry
from tmuxctl.server import (
    adopt,
    run,
    start_private_server,
)

socket = Path(os.environ["SOCK"])
workspace = Path(os.environ["WORK"])

start_private_server(
    socket,
    workspace,
)

initial = registry(socket)

assert {
    pane["window_name"]
    for pane in initial.values()
} == {
    "user",
    "agent",
    "logs",
}

assert adopt(socket) is True

print("M3 windows: PASS")
print("M3 adopt: PASS")

control = ControlClient(socket).start()

try:
    control_output = control.command(
        'list-windows -F "#{window_id}:#{window_name}"'
    )

    assert control_output.strip()
finally:
    control.close()

print("M3 control mode: PASS")

user_pane_id = next(
    pane_id
    for pane_id, pane in initial.items()
    if pane["window_name"] == "user"
)

user_window_id = initial[user_pane_id]["window_id"]

run(
    socket,
    "resize-window",
    "-t",
    user_window_id,
    "-x",
    "90",
    "-y",
    "30",
)

resize_deadline = time.monotonic() + 2.0
resized = False

while time.monotonic() < resize_deadline:
    current = registry(socket)
    user = current.get(user_pane_id)

    if (
        user is not None
        and user["width"] == 90
        and user["height"] == 30
    ):
        resized = True
        break

    time.sleep(0.05)

if not resized:
    current = registry(socket)
    raise AssertionError(
        "user pane did not report requested 90x30 window size; "
        f"current={current.get(user_pane_id)!r}"
    )

print("M3 resize reporting: PASS")

run(
    socket,
    "respawn-pane",
    "-k",
    "-t",
    user_pane_id,
    "sh",
    "-c",
    "exit 7",
)

exit_deadline = time.monotonic() + 2.0
dead = False

while time.monotonic() < exit_deadline:
    current = registry(socket)
    user = current.get(user_pane_id)

    if (
        user is not None
        and user["dead"] is True
    ):
        dead = True
        break

    time.sleep(0.05)

if not dead:
    current = registry(socket)
    raise AssertionError(
        "user pane did not enter remain-on-exit dead state; "
        f"current={current.get(user_pane_id)!r}"
    )

print("M3 pane process-exit reporting: PASS")
print("M3 PRIVATE TMUX: PASS")
PY

