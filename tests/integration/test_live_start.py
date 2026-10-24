import json
import os
import signal
import time
import urllib.request
from pathlib import Path

from cli.launch import live_start
from core.config import Config
from tmuxctl.server import kill_server, run


def test_live_start_reaches_ready(tmp_path: Path):
    home = tmp_path / "home"
    work = home / "work"
    work.mkdir(parents=True)
    runtime_root = Path(os.environ["PREFIX"]) / "tmp" / f"tca-live-it-{os.getpid()}"
    state_root = tmp_path / "state"
    env = dict(os.environ)
    env.update(HOME=str(home), PWD=str(work))
    payload = live_start(
        workspace=str(work),
        config=Config(state_root=str(state_root), runtime_root=str(runtime_root)),
        environ=env,
    )
    rt = Path(payload["paths"]["runtime_dir"])
    sock = Path(payload["paths"]["tmux_socket"])
    try:
        assert payload["status"] == "READY"
        state = json.loads(Path(payload["paths"]["state"]).read_text())
        assert state["status"] == "READY"
        assert (rt / "ctl.sock").is_socket()
        assert (rt / "heartbeat").is_file()
        assert (rt / "daemon.lock").is_file()
        names = run(sock, "list-windows", "-F", "#{window_name}").stdout.splitlines()
        assert set(names) == {"user", "agent", "logs"}
        with urllib.request.urlopen(payload["url"] + "health", timeout=1) as response:
            assert json.load(response)["ok"] is True
    finally:
        pid_file = rt / "daemon.pid"
        if pid_file.exists():
            try: os.kill(int(pid_file.read_text().strip()), signal.SIGTERM)
            except ProcessLookupError: pass
        kill_server(sock)
        for _ in range(30):
            if not (rt / "daemon.lock").exists(): break
            time.sleep(.1)
