#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$HOME/tmux-code-agent/tmux-code-agent-milestone-0"
VENV="$ROOT/.m0-venv"
LOCK="$ROOT/requirements.lock"

cd "$ROOT" || exit 1

echo '=== Q08 DEVICE A ==='

printf 'Model: '
getprop ro.product.model

printf 'Android: '
getprop ro.build.version.release

printf 'API: '
getprop ro.build.version.sdk

printf 'Architecture: '
uname -m

printf 'Python: '
python --version

echo
echo '=== LOCK ==='

sha256sum "$LOCK"

echo
echo '=== VENV ==='

test -x "$VENV/bin/python" || {
    echo 'FAIL: .m0-venv missing'
    exit 1
}

"$VENV/bin/python" - <<'PY'
import sys

print("executable:", sys.executable)
print("prefix:", sys.prefix)
print("base_prefix:", sys.base_prefix)
print("isolated:", sys.prefix != sys.base_prefix)

raise SystemExit(
    0 if sys.prefix != sys.base_prefix else 1
)
PY

echo
echo '=== PIP CHECK ==='

"$VENV/bin/python" -m pip check

echo
echo '=== REQUIRED PACKAGES ==='

"$VENV/bin/python" - <<'PY'
from importlib import metadata

names = (
    "starlette",
    "uvicorn",
    "websockets",
    "h11",
    "anyio",
)

failed = []

for name in names:
    try:
        version = metadata.version(name)
        print(f"PASS {name:12} {version}")
    except metadata.PackageNotFoundError:
        failed.append(name)
        print(f"FAIL {name:12} MISSING")

print()
print("Missing:", failed or "none")

raise SystemExit(1 if failed else 0)
PY

echo
echo 'Q08 DEVICE A: PASS'
