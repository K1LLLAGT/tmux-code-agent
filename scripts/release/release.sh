#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
src=${1:?source};out=${2:?output};tar -czf "$out" -C "$src" .;sha256sum "$out" > "$out.sha256";echo 'RELEASE: PASS'
