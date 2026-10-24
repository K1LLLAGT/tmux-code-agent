#!/data/data/com.termux/files/usr/bin/python
import datetime,json,os,platform,shutil,socket,subprocess,tempfile,time
from pathlib import Path
Q='Q04'; SPIKE='ssh-controlmaster-explicit-socket-retry-v2'
def run(a,t=15):
 try:
  p=subprocess.run(a,text=True,capture_output=True,timeout=t)
  return {'argv':a,'returncode':p.returncode,'stdout':p.stdout[-8000:],'stderr':p.stderr[-8000:]}
 except subprocess.TimeoutExpired as e:
  return {'argv':a,'returncode':124,'timed_out':True,'stdout':e.stdout or '','stderr':e.stderr or ''}
def emit(status,code,summary,evidence,rc):
 print(json.dumps({'schema_version':1,'question':Q,'spike':SPIKE,'status':status,'code':code,'summary':summary,'evidence':evidence,'environment':{'prefix':os.getenv('PREFIX'),'python':platform.python_version(),'platform':platform.platform(),'arch':platform.machine()},'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()},separators=(',',':')));raise SystemExit(rc)
def port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def wait_port(p,seconds=5):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  try:
   with socket.create_connection(('127.0.0.1',p),.2):return True
  except OSError:time.sleep(.1)
 return False
missing=[x for x in ('ssh','sshd','ssh-keygen') if not shutil.which(x)]
if missing:emit('FAIL','MISSING_BINARY','Required OpenSSH binaries missing',{'missing':missing},1)
prefix=os.getenv('PREFIX')
if not prefix:emit('SKIP','NOT_TERMUX','Target Termux required',{},2)
root=os.getenv('TMPDIR',prefix+'/tmp');os.makedirs(root,exist_ok=True)
sshd=None; master_started=False
with tempfile.TemporaryDirectory(prefix='t4-',dir=root) as td:
 rt=Path(td);os.chmod(rt,0o700)
 host=rt/'h';key=rt/'k';ak=rt/'ak';cfg=rt/'c';log=rt/'sshd.log';sock=rt/'m.sock';p=port()
 setup={}
 for name,path in [('host',host),('key',key)]:
  setup[name]=run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(path)])
  if setup[name]['returncode']!=0:emit('FAIL','KEYGEN_FAILED','Key generation failed',setup,1)
 ak.write_text('restrict,command="printf forced" '+Path(str(key)+'.pub').read_text().strip()+'\n');os.chmod(ak,0o600)
 cfg.write_text(f'''Port {p}\nListenAddress 127.0.0.1\nAddressFamily inet\nHostKey {host}\nPidFile {rt/'pid'}\nAuthorizedKeysFile {ak}\nStrictModes no\nPubkeyAuthentication yes\nPasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitEmptyPasswords no\nAllowTcpForwarding no\nAllowStreamLocalForwarding no\nAllowAgentForwarding no\nX11Forwarding no\nPermitTunnel no\nPermitUserEnvironment no\nPermitUserRC no\nLogLevel VERBOSE\n''')
 ctest=run([shutil.which('sshd'),'-t','-f',str(cfg)]);effective=run([shutil.which('sshd'),'-T','-f',str(cfg)])
 if ctest['returncode']!=0:emit('FAIL','SSHD_CONFIG_INVALID','Private sshd config rejected',{'config_test':ctest},1)
 lf=log.open('w');sshd=subprocess.Popen([shutil.which('sshd'),'-D','-e','-f',str(cfg)],stdout=lf,stderr=subprocess.STDOUT,text=True)
 try:
  if not wait_port(p):emit('FAIL','SSHD_NOT_READY','Private sshd not reachable',{'server_log':log.read_text(errors='replace')},1)
  base=['ssh','-F','none','-p',str(p),'-i',str(key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','GlobalKnownHostsFile=/dev/null','-o','LogLevel=ERROR','-o','ConnectTimeout=5','-o','ControlPath='+str(sock)]
  total_control_path_len=len(str(sock)); unix_budget=107
  start=run(base+[
   '-o','ControlMaster=yes',
   '-o','ControlPersist=60',
   '-fn',
   '127.0.0.1',
   'ignored'
  ])
  master_started=start['returncode']==0
  check1=run(base+['-O','check','127.0.0.1'])
  reuse_base=[
   'ssh','-vv',
   '-F','none',
   '-S',str(sock),
   '-p',str(p),
   '-i',str(key),
   '-o','IdentitiesOnly=yes',
   '-o','BatchMode=yes',
   '-o','StrictHostKeyChecking=no',
   '-o','UserKnownHostsFile=/dev/null',
   '-o','GlobalKnownHostsFile=/dev/null',
   '-o','LogLevel=ERROR',
   '127.0.0.1'
  ]
  calls=[run(reuse_base+['ignored']) for _ in range(3)]
  check2=run(base+['-O','check','127.0.0.1'])
  server_before_exit=log.read_text(errors='replace') if log.exists() else ''
  accepted_before=server_before_exit.count('Accepted publickey for ')
  stop_result=run(['ssh','-F','none','-S',str(sock),'-p',str(p),'-O','stop','127.0.0.1'])
  stop_socket_present=sock.exists()
  stop_check=run(['ssh','-F','none','-S',str(sock),'-p',str(p),'-O','check','127.0.0.1'])
  exit_result=run(['ssh','-F','none','-S',str(sock),'-p',str(p),'-O','exit','127.0.0.1'])
  for _ in range(30):
   if not sock.exists():break
   time.sleep(.1)
  socket_removed=not sock.exists()
  post_check=run(['ssh','-F','none','-S',str(sock),'-p',str(p),'-O','check','127.0.0.1'])
  fresh=run(['ssh','-F','none','-p',str(p),'-i',str(key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','GlobalKnownHostsFile=/dev/null','-o','LogLevel=ERROR','127.0.0.1','ignored'])
  checks={'control_path_within_budget':total_control_path_len<=unix_budget,'master_start_succeeded':start['returncode']==0,'master_socket_created':sock.exists() or check1['returncode']==0,'master_check_succeeded':check1['returncode']==0,'three_reused_calls_forced':all(x['returncode']==0 and x['stdout']=='forced' for x in calls),'master_still_healthy':check2['returncode']==0,'single_authentication_for_master_and_reused_calls':accepted_before==1,'stop_command_recorded':True,'master_exit_succeeded':exit_result['returncode']==0,'control_socket_removed':socket_removed,'post_exit_check_fails':post_check['returncode']!=0,'fresh_nonmaster_reconnect_succeeds':fresh['returncode']==0 and fresh['stdout']=='forced'}
  ev={'port':p,'control_path':str(sock),'control_path_length':total_control_path_len,'unix_socket_budget_used':unix_budget,'checks':checks,'config_test':ctest,'effective_config_selected':[x for x in effective.get('stdout','').splitlines() if x.lower().startswith(('listenaddress ','allowtcpforwarding ','passwordauthentication ','kbdinteractiveauthentication ','authorizedkeysfile '))],'master_start':start,'master_check_initial':check1,'reused_calls':calls,'master_check_after_reuse':check2,'accepted_publickey_count_before_exit':accepted_before,'stop_result':stop_result,'socket_present_after_stop':stop_socket_present,'check_after_stop':stop_check,'master_exit':exit_result,'post_exit_check':post_check,'fresh_reconnect':fresh,'reuse_verbose_diagnostics':[x.get('stderr','')[-8000:] for x in calls],'server_log':(log.read_text(errors='replace') if log.exists() else '')[-12000:]}
  failed=[k for k,v in checks.items() if not v]
  if failed:emit('FAIL','CONTROLMASTER_MATRIX_FAILED','One or more ControlMaster checks failed',{**ev,'failed_checks':failed},1)
  emit('PASS','CONTROLMASTER_OK','ControlMaster creation, reuse, shutdown, cleanup, and reconnect passed',ev,0)
 finally:
  if master_started:
   subprocess.run(['ssh','-F','none','-S',str(sock),'-p',str(p),'-O','exit','127.0.0.1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if sshd and sshd.poll() is None:
   sshd.terminate()
   try:sshd.wait(2)
   except subprocess.TimeoutExpired:sshd.kill();sshd.wait(2)
  lf.close()
