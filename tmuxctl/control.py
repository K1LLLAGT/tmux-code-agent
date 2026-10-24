from __future__ import annotations
import os,pty,select,subprocess,time
from pathlib import Path
class ControlClient:
 def __init__(self,socket:Path):self.socket=socket;self.proc=None;self.fd=None
 def start(self):
  master,slave=pty.openpty();self.proc=subprocess.Popen(['tmux','-S',str(self.socket),'-C','attach-session','-t','tca'],stdin=slave,stdout=slave,stderr=slave,close_fds=True);os.close(slave);self.fd=master;return self
 def command(self,command:str,timeout:float=1.0)->str:
  if self.fd is None:raise RuntimeError('control client not started')
  os.write(self.fd,(command+'\n').encode());end=time.monotonic()+timeout;buf=b''
  while time.monotonic()<end:
   r,_,_=select.select([self.fd],[],[],.1)
   if r:
    try:buf+=os.read(self.fd,65536)
    except OSError:break
    if b'%end' in buf or b'%error' in buf:break
  return buf.decode(errors='replace')
 def close(self):
  if self.proc and self.proc.poll() is None:self.proc.terminate();self.proc.wait(timeout=2)
  if self.fd is not None:
   try:os.close(self.fd)
   except OSError:pass
   self.fd=None
