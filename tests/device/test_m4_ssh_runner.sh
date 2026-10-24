#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}";PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}";cd "$ROOT"
rt="$PREFIX/tmp/tca-m4-dev-$$";sshdir="$rt/ssh";work="$rt/work";mkdir -p "$sshdir" "$work";chmod 700 "$rt" "$sshdir";echo nonce > "$rt/session.nonce";printf '%s\n' "$work" > "$rt/workspace"
cleanup(){ [ -n "${sshd_pid:-}" ]&&kill "$sshd_pid" 2>/dev/null||true;[ -n "${sshd_pid:-}" ]&&wait "$sshd_pid" 2>/dev/null||true;rm -rf "$rt";};trap cleanup EXIT
"$PY" - <<PY
from pathlib import Path
from transport.keys import generate_session_keys
from transport.config import authorized_keys,write_sshd_config
from supervisor.ports import reserve_loopback_port
rt=Path('$rt');d=rt/'ssh';k=generate_session_keys(d);(d/'authorized_keys').write_text(authorized_keys(Path(str(k['exec'])+'.pub').read_text(),Path(str(k['pty'])+'.pub').read_text(),Path('$ROOT/lib/tca-runner'),rt));(d/'authorized_keys').chmod(0o600);s,p=reserve_loopback_port();s.close();(rt/'port').write_text(str(p));write_sshd_config(d/'sshd_config',port=p,runtime=rt,host_key=k['host'],authorized=d/'authorized_keys')
PY
port=$(cat "$rt/port");ssh-keyscan -p "$port" 127.0.0.1 > "$sshdir/known_hosts" 2>/dev/null & scan=$! || true
"$(command -v sshd)" -D -e -f "$sshdir/sshd_config" >/dev/null 2>"$sshdir/sshd.log" & sshd_pid=$!
for i in $(seq 1 30);do if kill -0 "$sshd_pid" 2>/dev/null && ssh-keyscan -T 1 -p "$port" 127.0.0.1 > "$sshdir/known_hosts" 2>/dev/null;then break;fi;sleep .2;done
kill "$scan" 2>/dev/null||true;wait "$scan" 2>/dev/null||true
req="$rt/request.json";log="$rt/cmd";REQ="$req" LOG="$log" WORK="$work" "$PY" - <<'PY'
import json,os
from pathlib import Path
Path(os.environ['REQ']).write_text(json.dumps({'v':1,'command_id':'dev','argv':['sh','-c','printf hello; printf err >&2'],'cwd':os.environ['WORK'],'env':{'PATH':os.environ['PATH']},'timeout_s':3,'grace_s':.2,'max_output_bytes':4096,'log_dir':os.environ['LOG'],'stdin':None,'nonce':'nonce'}))
PY
out=$(cat "$req"|ssh -F none -p "$port" -i "$sshdir/exec_ed25519" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$sshdir/known_hosts" -o LogLevel=ERROR 127.0.0.1)
OUT="$out" "$PY" - <<'PY'
import json,os
r=json.loads(os.environ['OUT'].splitlines()[-1]);assert r['exit_code']==0;assert 'hello' in r['stdout_head'];assert 'err' in r['stderr_head'];print('M4 SSH RUNNER: PASS')
PY
