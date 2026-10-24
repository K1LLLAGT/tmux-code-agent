#!/data/data/com.termux/files/usr/bin/bash
set -u; . "$(dirname "$0")/common.sh"
is_termux || { emit Q06 browser-launch SKIP NOT_TERMUX 'Target Termux required' ''; exit 2; }
if command -v termux-open-url >/dev/null; then termux-open-url 'http://127.0.0.1:1/' >/dev/null 2>&1; emit Q06 browser-launch SKIP MANUAL_CONFIRMATION_REQUIRED 'Command invoked; actual opening requires manual confirmation' "command=$(command -v termux-open-url)"; exit 2; fi
emit Q06 browser-launch FAIL OPEN_URL_MISSING 'termux-open-url unavailable; print/copy fallback required' '';exit 1
