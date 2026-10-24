#!/data/data/com.termux/files/usr/bin/python
from common import *
import os,pty,select,subprocess,tempfile,time
if not termux(): emit('Q01','tmux-control-pty','SKIP','NOT_TERMUX','Target Termux required'); raise SystemExit(2)
with tempfile.TemporaryDirectory(dir=os.getenv('TMPDIR',os.environ['PREFIX']+'/tmp')) as d:
 s=d+'/tmux.sock'; evidence={"version":run(['tmux','-V'])}; subprocess.run(['tmux','-S',s,'-f','/dev/null','new-session','-d','-s','spike','sleep 30'])
 try:
  m,sl=pty.openpty(); p=subprocess.Popen(['tmux','-S',s,'-C','attach','-t','spike'],stdin=sl,stdout=sl,stderr=sl,close_fds=True); time.sleep(.5); r,_,_=select.select([m],[],[],2); data=os.read(m,8192).decode(errors='replace') if r else ''; p.terminate(); evidence['pty_output']=data[:2000]; ok='%begin' in data or '%session-changed' in data
  emit('Q01','tmux-control-pty','PASS' if ok else 'FAIL','CONTROL_FRAMES_OK' if ok else 'NO_CONTROL_FRAMES','tmux control mode over a PTY was exercised',evidence); raise SystemExit(0 if ok else 1)
 finally: subprocess.run(['tmux','-S',s,'kill-server'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
