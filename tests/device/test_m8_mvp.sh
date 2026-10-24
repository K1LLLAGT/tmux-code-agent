#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}";PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}";cd "$ROOT"
rt="$PREFIX/tmp/tca-m8-$$";mkdir -p "$rt/repo";trap 'rm -rf "$rt"' EXIT
git -C "$rt/repo" init -q;git -C "$rt/repo" config user.email a@b;git -C "$rt/repo" config user.name T;printf 'base\n' > "$rt/repo/a";git -C "$rt/repo" add a;git -C "$rt/repo" commit -qm init;printf 'user-change\n' > "$rt/repo/a"
RT="$rt" "$PY" - <<'PY'
import os
from pathlib import Path
from gitsafe.run import git
from audit.writer import AuditWriter
from audit.verify import verify
from store.db import open_db
from supervisor.recovery import classify
rt=Path(os.environ['RT']);repo=rt/'repo';before=(repo/'a').read_bytes();git(repo,'status','--porcelain=v2');assert (repo/'a').read_bytes()==before
log=rt/'events.jsonl';w=AuditWriter(log,'device');w.append('session.started',{});w.append('git.changed',{'count':1});assert verify(log)
c=open_db(rt/'state.db');assert c.execute('PRAGMA user_version').fetchone()[0]==1;c.close();assert classify(False,True)=='ORPHANED';print('M8 SM-T870 MVP CORE: PASS')
PY
bash install.sh --dry-run >/dev/null;bash uninstall.sh --dry-run >/dev/null
echo 'M8 INSTALLER SAFETY: PASS'
