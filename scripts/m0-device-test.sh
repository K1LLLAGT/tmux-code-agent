#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-milestone-0}"
LOCK="${ROOT}/requirements.lock"

model="$(getprop ro.product.model 2>/dev/null || true)"
manufacturer="$(getprop ro.product.manufacturer 2>/dev/null || true)"
android="$(getprop ro.build.version.release 2>/dev/null || true)"
sdk="$(getprop ro.build.version.sdk 2>/dev/null || true)"
fingerprint="$(getprop ro.build.fingerprint 2>/dev/null || true)"
arch="$(uname -m)"
python_version="$(python --version 2>&1)"

slug="$(
    printf '%s' "${manufacturer}-${model}" |
    tr '[:upper:]' '[:lower:]' |
    tr ' ' '-' |
    tr -cd 'a-z0-9._-'
)"

[ -n "$slug" ] || slug="unknown-device"

WORK="$HOME/tca-m0-device-test"
VENV="$WORK/.venv"
OUT="$WORK/evidence"

mkdir -p "$WORK" "$OUT"

if [ ! -f "$LOCK" ]; then
    echo "FAIL: missing requirements.lock:"
    echo "$LOCK"
    exit 1
fi

lock_sha256="$(
    sha256sum "$LOCK" |
    awk '{print $1}'
)"

echo '================================================'
echo 'TCA M0 DEVICE TEST'
echo '================================================'
echo "Device ID:     $slug"
echo "Manufacturer:  $manufacturer"
echo "Model:         $model"
echo "Android:       $android"
echo "API:           $sdk"
echo "Architecture:  $arch"
echo "Python:        $python_version"
echo "Lock SHA-256:  $lock_sha256"
echo

rm -rf "$VENV"

echo '=== CREATE VENV ==='

python -m venv "$VENV"
venv_rc=$?

if [ "$venv_rc" -ne 0 ]; then
    install_rc=1
    check_rc=1
else
    echo
    echo '=== INSTALL REQUIREMENTS ==='

    "$VENV/bin/python" -m pip install \
        -r "$LOCK"

    install_rc=$?

    if [ "$install_rc" -eq 0 ]; then
        echo
        echo '=== PIP CHECK ==='

        "$VENV/bin/python" -m pip check
        check_rc=$?
    else
        check_rc=1
    fi
fi

if [ -x "$VENV/bin/python" ]; then
    "$VENV/bin/python" -m pip freeze \
        > "$OUT/q08-freeze.txt" 2>&1 || true
else
    : > "$OUT/q08-freeze.txt"
fi

echo
echo '=== WRITE EVIDENCE ==='

DEVICE_ID="$slug" \
DEVICE_MANUFACTURER="$manufacturer" \
DEVICE_MODEL="$model" \
DEVICE_ANDROID="$android" \
DEVICE_SDK="$sdk" \
DEVICE_ARCH="$arch" \
DEVICE_FINGERPRINT="$fingerprint" \
LOCK_SHA256="$lock_sha256" \
VENV_RC="$venv_rc" \
INSTALL_RC="$install_rc" \
CHECK_RC="$check_rc" \
OUT_DIR="$OUT" \
"$VENV/bin/python" - <<'PY'
import hashlib
import json
import os
import platform
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

required = (
    "starlette",
    "uvicorn",
    "websockets",
    "h11",
    "anyio",
)

packages = []

for name in required:
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        version = None

    packages.append({
        "name": name,
        "version": version,
    })

missing = [
    item["name"]
    for item in packages
    if item["version"] is None
]

venv_rc = int(os.environ["VENV_RC"])
install_rc = int(os.environ["INSTALL_RC"])
check_rc = int(os.environ["CHECK_RC"])

physical_facts = "|".join([
    os.environ["DEVICE_MANUFACTURER"],
    os.environ["DEVICE_MODEL"],
    os.environ["DEVICE_FINGERPRINT"],
])

physical_device_id = hashlib.sha256(
    physical_facts.encode()
).hexdigest()[:16]

passed = (
    venv_rc == 0
    and install_rc == 0
    and check_rc == 0
    and not missing
)

result = {
    "schema_version": 1,
    "question": "Q08",
    "spike": "dependency-install-device",
    "status": "PASS" if passed else "FAIL",
    "code": (
        "DEVICE_INSTALL_OK"
        if passed
        else "DEVICE_INSTALL_FAILED"
    ),
    "summary": (
        "Pinned dependencies installed and validated "
        "on this physical Android/Termux device."
        if passed
        else
        "Dependency validation failed on this device."
    ),
    "evidence": {
        "physical_device": True,
        "physical_device_id": physical_device_id,
        "device_slug": os.environ["DEVICE_ID"],
        "manufacturer": os.environ["DEVICE_MANUFACTURER"],
        "model": os.environ["DEVICE_MODEL"],
        "android_release": os.environ["DEVICE_ANDROID"],
        "android_sdk": os.environ["DEVICE_SDK"],
        "android_fingerprint": os.environ["DEVICE_FINGERPRINT"],
        "architecture": os.environ["DEVICE_ARCH"],
        "python": platform.python_version(),
        "requirements_lock_sha256": os.environ["LOCK_SHA256"],
        "venv_returncode": venv_rc,
        "install_returncode": install_rc,
        "pip_check_returncode": check_rc,
        "packages": packages,
        "missing_packages": missing,
        "freeze_file": "q08-freeze.txt",
    },
    "runner_exit_code": 0 if passed else 1,
    "timestamp": datetime.now(
        timezone.utc
    ).isoformat(),
}

out = Path(os.environ["OUT_DIR"])

(out / "q08.json").write_text(
    json.dumps(result, indent=2) + "\n"
)

device = {
    "schema_version": 1,
    "physical_device_id": physical_device_id,
    "device_slug": os.environ["DEVICE_ID"],
    "manufacturer": os.environ["DEVICE_MANUFACTURER"],
    "model": os.environ["DEVICE_MODEL"],
    "android_release": os.environ["DEVICE_ANDROID"],
    "android_sdk": os.environ["DEVICE_SDK"],
    "android_fingerprint": os.environ["DEVICE_FINGERPRINT"],
    "architecture": os.environ["DEVICE_ARCH"],
    "python": platform.python_version(),
}

(out / "device.json").write_text(
    json.dumps(device, indent=2) + "\n"
)

print(json.dumps(result, indent=2))

raise SystemExit(0 if passed else 1)
PY

result_rc=$?

cd "$OUT" || exit 1

sha256sum \
    device.json \
    q08.json \
    q08-freeze.txt \
    > SHA256SUMS

echo
echo '=== EVIDENCE ==='
pwd
cat SHA256SUMS

exit "$result_rc"
