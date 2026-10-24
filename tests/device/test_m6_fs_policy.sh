#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}";PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}";cd "$ROOT"
work="$PREFIX/tmp/tca-m6-$$";mkdir -p "$work/ws" "$work/out";trap 'rm -rf "$work"' EXIT
WORK="$work" "$PY" - <<'PY'
import os
from pathlib import Path
from tools.fs_tools import write_file,read_file
from fsguard.safeio import open_read
from policy.capabilities import Capability as C,Decision as D
from policy.profiles import decision
from policy.approvals import request,valid
base=Path(os.environ['WORK']);w=base/'ws';outside=base/'out'/'secret';outside.write_text('NO')
r=write_file(w,'hello.txt','hello');assert r['ok'];h=r['data']['sha256'];assert read_file(w,'hello.txt')['data']['content']=='hello';assert write_file(w,'hello.txt','changed','wrong')['error']['code']=='ERR_STALE_FILE';assert write_file(w,'hello.txt','changed',h)['ok']
(w/'escape').symlink_to(outside)
try:open_read('escape',w);raise AssertionError('symlink escape opened')
except Exception:pass
assert decision('READ_ONLY',C.FS_WRITE)==D.DENY;assert decision('SAFE',C.FS_WRITE)==D.APPROVE;assert decision('NORMAL',C.FS_WRITE)==D.ALLOW
a=request('write_file',{'path':'hello.txt'},str(w));assert valid(a,'write_file',{'path':'hello.txt'},str(w));assert not valid(a,'write_file',{'path':'other.txt'},str(w))
print('M6 FILESYSTEM/POLICY: PASS')
PY
