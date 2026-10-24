#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
python - <<'PY'
import tempfile
from pathlib import Path
from core.releases import flip
r=Path(tempfile.mkdtemp());(r/'releases/a').mkdir(parents=True);(r/'releases/b').mkdir();flip(r,'a');flip(r,'b');assert (r/'current').resolve().name=='b';print('M13 UPGRADE/ROLLBACK: PASS')
PY
