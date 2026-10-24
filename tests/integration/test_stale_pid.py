import json
from supervisor.lock import acquire_lock,read_pid
def test_stale_pid_replaced(tmp_path):
 p=tmp_path/'lock';p.write_text(json.dumps({'pid':99999999}));acquire_lock(p,pid=12345);assert read_pid(p)==12345
