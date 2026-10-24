#!/data/data/com.termux/files/usr/bin/bash
set -u
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd); repo=$(CDPATH= cd -- "$base/../.." && pwd); cd "$repo"
device=${TCA_DEVICE_ID:-$(uname -m 2>/dev/null)-$(getprop ro.build.version.sdk 2>/dev/null || echo unknown)}
out="docs/spike-results/${device}.jsonl"; mkdir -p "$(dirname "$out")"; : >"$out"; rc=0
for s in "$base"/q*.py "$base"/q*.sh; do [ -e "$s" ] || continue; case "$s" in *.py) cmd=(python "$s");; *) cmd=(bash "$s");; esac; "${cmd[@]}" >>"$out" || rc=1; done
python "$base/validate-results.py" "$out" || rc=1
exit "$rc"
