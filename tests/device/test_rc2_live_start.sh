#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}"
cd "$ROOT"
out="$PREFIX/tmp/tca-rc2-live-start.json"
./tmux-code-agent start --json > "$out"
"$ROOT/.m0-venv/bin/python" - "$out" <<'PY'
import json,os,signal,sys,time,urllib.request
from pathlib import Path
from tmuxctl.server import kill_server,run
p=json.loads(Path(sys.argv[1]).read_text());rt=Path(p['paths']['runtime_dir']);sock=Path(p['paths']['tmux_socket'])
assert p['status']=='READY';assert sock.exists();assert (rt/'ctl.sock').is_socket();assert (rt/'heartbeat').exists();assert (rt/'daemon.lock').exists()
assert set(run(sock,'list-windows','-F','#{window_name}').stdout.splitlines())=={'user','agent','logs'}
with urllib.request.urlopen(p['url']+'health',timeout=1) as r: assert json.load(r)['ok'] is True
print('RC2 LIVE START: PASS')
pid=int((rt/'daemon.pid').read_text());os.kill(pid,signal.SIGTERM);kill_server(sock)
for _ in range(30):
 if not (rt/'daemon.lock').exists():break
 time.sleep(.1)
PY
rm -f "$out"
