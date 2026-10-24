#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="${TCA_ROOT:-$HOME/tmux-code-agent/tmux-code-agent-v1}";PY="${TCA_PYTHON:-$ROOT/.m0-venv/bin/python}";cd "$ROOT"
rt="$PREFIX/tmp/tca-m7-$$";mkdir -p "$rt";trap 'kill ${srv:-} 2>/dev/null||true; wait ${srv:-} 2>/dev/null||true; rm -rf "$rt"' EXIT
port=$($PY - <<'PY'
from supervisor.ports import reserve_loopback_port
s,p=reserve_loopback_port();print(p);s.close()
PY
)
script='[{"tool":"echo","args":{"value":"phone"}},{"tool":"finish","args":{"summary":"device smoke","claims":[]}}]'
"$PY" tests/fixtures/fake_model_server.py --port "$port" --script "$script" & srv=$!
for i in $(seq 1 30);do "$PY" - <<PY >/dev/null 2>&1 && break || true
import urllib.request,json
json.load(urllib.request.urlopen('http://127.0.0.1:$port/v1/models',timeout=.2))
PY
sleep .1;done
PORT="$port" "$PY" - <<'PY'
import asyncio,os
from agent.engine import AgentEngine
from models.openai_compat import OpenAICompatProvider
p=OpenAICompatProvider(f"http://127.0.0.1:{os.environ['PORT']}/v1",'fake-model');seen=[]
def dispatch(name,args):seen.append((name,args));return {'ok':True,'data':args}
r=asyncio.run(AgentEngine(p,dispatch).run('device smoke','README.md'));assert r['ok'];assert seen==[('echo',{'value':'phone'})];assert r['summary']=='device smoke';print('M7 MODEL/AGENT: PASS')
PY
