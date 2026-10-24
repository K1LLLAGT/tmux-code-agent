import os
from pathlib import Path
from tmuxctl.server import start_private_server,kill_server,run
from termbridge.viewer import create_viewer,destroy_viewer
def test_grouped_viewer(tmp_path):
 s=Path(os.environ['PREFIX'])/'tmp'/f'tca-m5-view-{os.getpid()}.sock';w=tmp_path/'w';w.mkdir();name=None
 try:
  start_private_server(s,w);name=create_viewer(s,'user');p=run(s,'list-sessions','-F','#{session_name}:#{session_grouped}');assert name in p.stdout
 finally:
  if name:destroy_viewer(s,name)
  kill_server(s);s.unlink(missing_ok=True)
