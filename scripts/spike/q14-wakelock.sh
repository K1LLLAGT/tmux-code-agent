#!/data/data/com.termux/files/usr/bin/bash
set -u; . "$(dirname "$0")/common.sh"
emit Q14 wakelock SKIP MANUAL_CHECK_REQUIRED 'Manual screen-off wake-lock soak required' 'Use docs/manual-Q14.md'; exit 2
