import os
from pathlib import Path
from tmuxctl.server import start_private_server,kill_server
from tmuxctl.panes import list_panes
def test_private_server(tmp_path):
 s=Path(os.environ['PREFIX'])/'tmp'/f'tca-m3-pytest-{os.getpid()}.sock';work=tmp_path/'w';work.mkdir()
 try:
  start_private_server(s,work);panes=list_panes(s);assert {p.window_name for p in panes}=={'user','agent','logs'};assert all(not p.dead for p in panes)
 finally:kill_server(s);s.unlink(missing_ok=True)
