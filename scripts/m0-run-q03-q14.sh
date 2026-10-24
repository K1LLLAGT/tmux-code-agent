#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail
ROOT="${ROOT:-$HOME/tmux-code-agent/tmux-code-agent-milestone-0}"
DEVICE="${TCA_DEVICE_ID:-sm-t870}"
SPIKE="$ROOT/scripts/spike"
OUT="$ROOT/docs/spike-results"
LOG="$OUT/logs/$DEVICE"
mkdir -p "$OUT" "$LOG"
cd "$ROOT" || exit 1
run_one() {
  local q="$1" file base json stdout stderr rc
  file="$(find "$SPIKE" -maxdepth 1 -type f \( -iname "${q}-*.sh" -o -iname "${q}-*.py" \) -print -quit)"
  if [ -z "$file" ]; then echo "[$q] MISSING"; return 1; fi
  base="$DEVICE-${q,,}"
  json="$OUT/$base.json"; stdout="$LOG/$base.stdout"; stderr="$LOG/$base.stderr"
  echo "=== $q: $(basename "$file") ==="
  if [[ "$file" == *.py ]]; then python "$file" >"$stdout" 2>"$stderr"; rc=$?; else bash "$file" >"$stdout" 2>"$stderr"; rc=$?; fi
  python - "$stdout" "$json" "$q" "$rc" "$stderr" <<'PY'
import json,sys,datetime,pathlib
src,out,q,rc,err=sys.argv[1:]
lines=pathlib.Path(src).read_text(errors='replace').splitlines()
obj=None
for line in reversed(lines):
    try:
        x=json.loads(line)
        if isinstance(x,dict): obj=x; break
    except Exception: pass
if obj is None:
    obj={"schema_version":1,"question":q,"spike":"runner-wrapper","status":"FAIL","code":"NO_JSON_RESULT","summary":"Probe did not emit a JSON object","evidence":{"stdout":"\n".join(lines)[-8000:],"stderr":pathlib.Path(err).read_text(errors='replace')[-8000:]},"environment":{},"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()}
obj["runner_exit_code"]=int(rc)
pathlib.Path(out).write_text(json.dumps(obj,indent=2)+"\n")
print(f'{q}: {obj.get("status")} / {obj.get("code")} / exit={rc}')
PY
  return 0
}
for q in Q03 Q04 Q05 Q06 Q07 Q08 Q09 Q10 Q11 Q12 Q13 Q14; do run_one "$q" || true; done
python "$ROOT/scripts/m0-review-results.py" "$DEVICE"
echo "Evidence: $OUT/$DEVICE-q03.json through $DEVICE-q14.json"
echo "Logs: $LOG"
echo 'Milestone 1 remains NOT STARTED.'
