#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}"
A="$ROOT/android"
OUT="$ROOT/dist"
NAME="tmux-code-agent-v1.0.0-rc2.apk"
cd "$A"
command -v java >/dev/null
if [ -x ./gradlew ]; then G=./gradlew; elif command -v gradle >/dev/null; then G=gradle; else echo 'STOP: Gradle not found. Install/provide Gradle 9.1.0 or add a verified Gradle wrapper.' >&2; exit 2; fi
"$G" --no-daemon clean assembleDebug
src="app/build/outputs/apk/debug/app-debug.apk"
test -f "$src"
mkdir -p "$OUT"
cp "$src" "$OUT/$NAME"
sha256sum "$OUT/$NAME" | tee "$OUT/$NAME.sha256"
echo "RC2 APK BUILT: $OUT/$NAME"
