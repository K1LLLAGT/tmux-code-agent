#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP_ROOT="$HOME/.local/share/tmux-code-agent"
TARGET="$APP_ROOT/current"
LOCAL_SHARE="$HOME/.local/share"
LOCAL_ROOT="$HOME/.local"

dry_run=0

if [ "${1:-}" = "--dry-run" ]; then
    dry_run=1
elif [ "$#" -ne 0 ]; then
    printf 'Usage: %s [--dry-run]\n' "$0" >&2
    exit 2
fi

printf 'Would remove app link: %s\n' "$TARGET"
printf '%s\n' 'Projects, ~/.ssh and user tmux are not touched.'

if [ "$dry_run" -eq 1 ]; then
    exit 0
fi

if [ -L "$TARGET" ]; then
    rm -- "$TARGET"
elif [ -e "$TARGET" ]; then
    printf 'ERROR: refusing to remove non-symlink target: %s\n' \
      "$TARGET" >&2
    exit 1
fi

# Remove installer-created directories only when they are empty.
# Bottom-up rmdir preserves unrelated files and existing user directories.
rmdir -- "$APP_ROOT" 2>/dev/null || true
rmdir -- "$LOCAL_SHARE" 2>/dev/null || true
rmdir -- "$LOCAL_ROOT" 2>/dev/null || true

printf '%s\n' 'UNINSTALL: PASS'
