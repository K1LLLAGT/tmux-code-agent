import os
from pathlib import Path
from tmuxctl.server import start_private_server,kill_server
from tmuxctl.control import ControlClient
def test_control_client(tmp_path):
 s=Path(os.environ['PREFIX'])/'tmp'/f'tca-m3-ctl-{os.getpid()}.sock';w=tmp_path/'w';w.mkdir();c=None
 try:
  start_private_server(s,w);c=ControlClient(s).start();out=c.command('list-panes -a -F "#{pane_id}"');assert '%begin' in out or '%end' in out
 finally:
  if c:c.close()
  kill_server(s);s.unlink(missing_ok=True)
