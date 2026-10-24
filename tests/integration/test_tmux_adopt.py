import os
from pathlib import Path
from tmuxctl.server import start_private_server,kill_server,adopt
def test_adopt(tmp_path):
 s=Path(os.environ['PREFIX'])/'tmp'/f'tca-m3-adopt-{os.getpid()}.sock';w=tmp_path/'w';w.mkdir()
 try:start_private_server(s,w);assert adopt(s)
 finally:kill_server(s);s.unlink(missing_ok=True)
