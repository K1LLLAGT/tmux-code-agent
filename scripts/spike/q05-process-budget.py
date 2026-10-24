#!/data/data/com.termux/files/usr/bin/python
from common import *
import os,subprocess,time
if not termux(): emit('Q05','process-budget','SKIP','NOT_TERMUX','Target Termux required'); raise SystemExit(2)
children=[]; ev={'baseline':run(['sh','-c',"ps -A 2>/dev/null | wc -l"])}
try:
 for _ in range(16): children.append(subprocess.Popen(['sleep','3']))
 time.sleep(.3); alive=sum(p.poll() is None for p in children); ev['spawned']=16;ev['alive']=alive
 emit('Q05','process-budget','PASS' if alive==16 else 'FAIL','BOUNDED_FANOUT_OK' if alive==16 else 'CHILD_LOSS','A conservative bounded process fan-out was measured',ev); raise SystemExit(0 if alive==16 else 1)
finally:
 for p in children:
  if p.poll() is None:p.terminate()
