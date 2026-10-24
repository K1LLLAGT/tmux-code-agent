#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)";dry=0;[ "${1:-}" = --dry-run ]&&dry=1
TARGET="$HOME/.local/share/tmux-code-agent/current";echo "TCA install source: $ROOT";echo "TCA target: $TARGET";[ "$dry" -eq 1 ]&&exit 0
mkdir -p "$HOME/.local/share/tmux-code-agent";ln -sfn "$ROOT" "$TARGET";echo 'INSTALL: PASS'
