#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
python - <<'PY'
from models.llamacpp import LlamaCppCaps
assert LlamaCppCaps.context({'n_ctx':4096})==4096;print('M12 PROVIDERS: PASS')
PY
