import os
from supervisor.lock import acquire_lock,read_pid,release_lock
def test_lock(tmp_path):
 p=tmp_path/'lock';acquire_lock(p);assert read_pid(p)==os.getpid();release_lock(p);assert not p.exists()
