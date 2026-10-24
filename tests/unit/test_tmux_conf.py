import stat
from tmuxctl.conf import write_config
def test_config(tmp_path):
 p=write_config(tmp_path/'tmux.conf');assert 'status off' in p.read_text();assert stat.S_IMODE(p.stat().st_mode)==0o600
