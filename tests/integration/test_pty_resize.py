import os,struct,termios,fcntl,time
from termbridge.pty_bridge import PtyProcess
def test_resize_propagates():
 p=PtyProcess.spawn(['sh','-c','sleep 2']);
 try:
  p.resize(91,31);rows,cols,_,_=struct.unpack('HHHH',fcntl.ioctl(p.master,termios.TIOCGWINSZ,b'\0'*8));assert (cols,rows)==(91,31)
 finally:p.close()
