#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}"
PYTHON="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}"
cd "$ROOT"
work="$PREFIX/tmp/tca-m1-device-$$"
mkdir -p "$work/project"
out="$work/out.json"
cleanup() {
  if [ -f "$out" ]; then
    state_dir=$("$PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1]))["paths"]["state_dir"])' "$out" 2>/dev/null || true)
    runtime_dir=$("$PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1]))["paths"]["runtime_dir"])' "$out" 2>/dev/null || true)
    [ -n "${state_dir:-}" ] && rm -rf "$state_dir"
    [ -n "${runtime_dir:-}" ] && rm -rf "$runtime_dir"
  fi
  rm -rf "$work"
}
trap cleanup EXIT
(
  cd "$work/project"
  API_TOKEN='M1_DEVICE_SECRET_456' "$ROOT/tmux-code-agent" start --dry-run --json > "$out"
)
"$PYTHON" -m json.tool "$out" >/dev/null
! grep -R -F 'M1_DEVICE_SECRET_456' "$out" "$HOME/.local/state/tmux-code-agent/sessions" 2>/dev/null
"$PYTHON" - <<'PY' "$out"
import json, os, stat, sys
from pathlib import Path
p=json.load(open(sys.argv[1]))
assert p['dry_run'] is True
assert p['manifest']['workspace']==str(Path(os.environ['PREFIX'])/'tmp'/Path(sys.argv[1]).parent.name/'project') or p['manifest']['workspace'].endswith('/project')
assert stat.S_IMODE(Path(p['paths']['manifest']).stat().st_mode)==0o400
assert stat.S_IMODE(Path(p['paths']['state']).stat().st_mode)==0o600
print('M1 DEVICE DRY RUN: PASS')
PY
