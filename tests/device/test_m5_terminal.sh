#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}";PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}";cd "$ROOT"
rt="$PREFIX/tmp/tca-m5-dev-$$";sock="$rt/tmux.sock";work="$rt/work";mkdir -p "$work"
cleanup(){ tmux -S "$sock" kill-server 2>/dev/null||true;rm -rf "$rt";};trap cleanup EXIT
SOCK="$sock" WORK="$work" "$PY" - <<'PY'
import os,subprocess,time
from pathlib import Path
from tmuxctl.server import start_private_server,run
from termbridge.viewer import create_viewer,destroy_viewer
from web.ws_events import EventRing
from web.ws_term import BackpressureGate
s=Path(os.environ['SOCK']);w=Path(os.environ['WORK']);start_private_server(s,w);viewer=create_viewer(s,'user');sessions=run(s,'list-sessions','-F','#{session_name}').stdout;assert viewer in sessions
# Real tmux process survives viewer destruction/recreation.
user=next(line.split('\t')[0] for line in run(s,'list-panes','-a','-F','#{pane_id}\t#{window_name}').stdout.splitlines() if line.endswith('\tuser'))
run(s,'send-keys','-t',user,'printf M5_ALIVE; sleep 1','Enter');destroy_viewer(s,viewer);viewer=create_viewer(s,'user');time.sleep(.2);assert viewer in run(s,'list-sessions','-F','#{session_name}').stdout
# Event replay and 1 GiB logical pending-buffer gate without allocating 1 GiB.
r=EventRing(4);r.publish('terminal.attached',{'viewer':viewer});assert r.replay(0)[0]['seq']==1
g=BackpressureGate();assert g.update(1024**3) is True;assert g.update(0) is False
print('M5 TERMINAL CHANNEL: PASS')
destroy_viewer(s,viewer)
PY
