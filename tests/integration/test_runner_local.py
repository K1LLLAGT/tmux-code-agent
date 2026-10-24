import json,os,subprocess
from pathlib import Path

def setup_rt(tmp_path):
 rt=tmp_path/'rt';rt.mkdir();w=tmp_path/'w';w.mkdir();(rt/'session.nonce').write_text('n');(rt/'workspace').write_text(str(w));return rt,w

def invoke(rt,w,log,argv,timeout=2,maxb=10000):
 req={'v':1,'command_id':'c1','argv':argv,'cwd':str(w),'env':{'PATH':os.environ['PATH']},'timeout_s':timeout,'grace_s':.1,'max_output_bytes':maxb,'log_dir':str(log),'stdin':None,'nonce':'n'}
 return subprocess.run(['lib/tca-runner',str(rt)],input=json.dumps(req),text=True,capture_output=True)

def test_runner_stdout_stderr(tmp_path):
 rt,w=setup_rt(tmp_path);p=invoke(rt,w,tmp_path/'log',['sh','-c','echo out; echo err >&2']);r=json.loads(p.stdout);assert r['exit_code']==0 and 'out' in r['stdout_head'] and 'err' in r['stderr_head'];assert (tmp_path/'log'/'result.json').exists()
def test_runner_timeout(tmp_path):
 rt,w=setup_rt(tmp_path);p=invoke(rt,w,tmp_path/'log',['sh','-c','sleep 5'],timeout=.1);r=json.loads(p.stdout);assert r['timed_out'] is True
def test_runner_cwd_guard(tmp_path):
 rt,w=setup_rt(tmp_path);req={'v':1,'command_id':'c','argv':['true'],'cwd':'/','env':{},'timeout_s':1,'grace_s':.1,'max_output_bytes':100,'log_dir':str(tmp_path/'l'),'nonce':'n'};p=subprocess.run(['lib/tca-runner',str(rt)],input=json.dumps(req),text=True,capture_output=True);assert p.returncode!=0
def test_runner_output_cap(tmp_path):
 rt,w=setup_rt(tmp_path);p=invoke(rt,w,tmp_path/'log',['sh','-c','yes X | head -c 10000'],maxb=1000);r=json.loads(p.stdout);assert r['truncated'] is True
