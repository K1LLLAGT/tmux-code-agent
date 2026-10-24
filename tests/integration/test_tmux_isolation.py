import os,subprocess
from pathlib import Path
from tmuxctl.server import start_private_server,kill_server
def test_private_socket_is_explicit(tmp_path):
 s=Path(os.environ['PREFIX'])/'tmp'/f'tca-m3-iso-{os.getpid()}.sock';w=tmp_path/'w';w.mkdir()
 try:
  start_private_server(s,w);p=subprocess.run(['tmux','-S',str(s),'display-message','-p','#{socket_path}'],text=True,capture_output=True,check=True);assert p.stdout.strip()==str(s)
 finally:kill_server(s);s.unlink(missing_ok=True)
