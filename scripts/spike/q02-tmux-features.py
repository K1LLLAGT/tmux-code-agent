#!/data/data/com.termux/files/usr/bin/python
from common import *
import os,tempfile,subprocess
if not termux(): emit('Q02','tmux-features','SKIP','NOT_TERMUX','Target Termux required'); raise SystemExit(2)
with tempfile.TemporaryDirectory(dir=os.getenv('TMPDIR',os.environ['PREFIX']+'/tmp')) as d:
 s=d+'/t.sock'; ev={'version':run(['tmux','-V'])};
 tests={
 'new_session_e':['tmux','-S',s,'-f','/dev/null','new-session','-d','-s','a','-e','TCA_SPIKE=1','sleep 5'],
 'pause_after':['tmux','-S',s,'-f','/dev/null','new-session','-d','-s','b','-f','pause-after=1','sleep 5']}
 for k,v in tests.items(): ev[k]=run(v)
 ev['refresh_client_no_output']=run(['tmux','-S',s,'refresh-client','-f','no-output'])
 subprocess.run(['tmux','-S',s,'kill-server'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 emit('Q02','tmux-features','PASS','FEATURES_RECORDED','tmux features were feature-detected; unsupported features require documented fallback',ev)
