#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
python - <<'PY'
from gitsafe.worktree import should_offer
assert should_offer(True);print('M11 WORKTREE/BUNDLE: PASS')
PY
