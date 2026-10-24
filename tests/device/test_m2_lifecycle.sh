#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}"
PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}"

cd "$ROOT"

rt="$PREFIX/tmp/tca-m2-$$"
mkdir -p "$rt"

port="$(
"$PY" - <<'PY'
from supervisor.ports import reserve_loopback_port

sock, port = reserve_loopback_port()
print(port)
sock.close()
PY
)"

PYTHONPATH="$ROOT" \
"$PY" -m supervisor.daemon \
  --runtime "$rt" \
  --port "$port" &

pid=$!

cleanup() {
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  rm -rf "$rt"
}

trap cleanup EXIT

ready=0

for i in $(seq 1 30); do
  if PORT="$port" "$PY" - <<'PY'
import json
import os
import urllib.error
import urllib.request

port = os.environ["PORT"]

try:
    with urllib.request.urlopen(
        f"http://127.0.0.1:{port}/health",
        timeout=0.3,
    ) as response:
        payload = json.load(response)
except (urllib.error.URLError, TimeoutError, OSError):
    raise SystemExit(1)

raise SystemExit(
    0 if payload.get("ok") is True else 1
)
PY
  then
    ready=1
    break
  fi

  sleep 0.2
done

if [ "$ready" -ne 1 ]; then
  echo "FAIL: M2 daemon did not become ready" >&2
  exit 1
fi

echo "M2 health: READY"

kill -0 "$pid"

test -S "$rt/ctl.sock"
test -f "$rt/daemon.lock"
test -f "$rt/heartbeat"

kill "$pid"
wait "$pid" || true

echo "M2 DEVICE LIFECYCLE: PASS"

