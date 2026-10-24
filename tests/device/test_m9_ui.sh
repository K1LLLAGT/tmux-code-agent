#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
grep -q 'tablet' frontend/src/components/v1_panels.js;grep -q 'Settings' frontend/src/components/v1_panels.js;echo 'M9 UI AREAS: PASS'
