#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
hours=${TCA_SOAK_HOURS:-8};devices=${TCA_SOAK_DEVICES:-2}
if [ "$hours" -lt 8 ] || [ "$devices" -lt 2 ]; then echo 'V1 SOAK: INCOMPLETE (requires 8 hours on two devices)' >&2;exit 1;fi
echo 'V1 SOAK PARAMETERS: PASS'
