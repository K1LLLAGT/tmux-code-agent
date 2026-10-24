#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
TARGET="$HOME/.local/share/tmux-code-agent/current";dry=0;[ "${1:-}" = --dry-run ]&&dry=1;echo "Would remove app link: $TARGET";echo 'Projects, ~/.ssh and user tmux are not touched.';[ "$dry" -eq 1 ]&&exit 0;rm -f "$TARGET";echo 'UNINSTALL: PASS'
