from __future__ import annotations
import fcntl,os,pty,struct,subprocess,termios
from dataclasses import dataclass
@dataclass(slots=True)
class PtyProcess:
 proc:subprocess.Popen; master:int
 @classmethod
 def spawn(cls,argv:list[str],env=None):
  master,slave=pty.openpty();p=subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=slave,close_fds=True,start_new_session=True,env=env);os.close(slave);return cls(p,master)
 def resize(self,cols:int,rows:int):fcntl.ioctl(self.master,termios.TIOCSWINSZ,struct.pack('HHHH',rows,cols,0,0))
 def write(self,data:bytes):return os.write(self.master,data)
 def read(self,size=65536):return os.read(self.master,size)
 def close(self):
  if self.proc.poll() is None:self.proc.terminate()
  try:self.proc.wait(timeout=2)
  except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(timeout=2)
  try:os.close(self.master)
  except OSError:pass
