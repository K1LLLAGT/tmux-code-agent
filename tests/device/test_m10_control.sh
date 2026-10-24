#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
python - <<'PY'
from policy.v1 import yolo_grants_root
from agent.ownership import Ownership,PaneOwned
assert not yolo_grants_root();o=Ownership();o.take()
try:o.agent_write('agent');raise AssertionError
except PaneOwned:pass
print('M10 YOLO/CONTROL: PASS')
PY
