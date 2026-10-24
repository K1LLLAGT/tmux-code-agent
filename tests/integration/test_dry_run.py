import json
import os
import stat
import tempfile
from pathlib import Path

from cli.launch import dry_run_start
from core.config import Config


def test_dry_run_creates_safe_snapshot_without_secret(tmp_path: Path) -> None:
    home = tmp_path / "home"
    workspace = home / "projects" / "x"
    workspace.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="m1-it-", dir=os.environ.get("TMPDIR", "/tmp")) as d:
        runtime_root = Path(d)
        state_root = tmp_path / "state"
        env = {
            "HOME": str(home), "PREFIX": str(runtime_root.parent), "PWD": str(workspace),
            "PATH": os.environ["PATH"], "SHELL": "/bin/zsh", "TERM": "xterm",
            "API_TOKEN": "M1_SECRET_FIXTURE_123",
        }
        payload = dry_run_start(
            workspace=str(workspace),
            config=Config(state_root=str(state_root), runtime_root=str(runtime_root)),
            environ=env,
        )
        state_dir = Path(payload["paths"]["state_dir"])
        manifest = Path(payload["paths"]["manifest"])
        state = Path(payload["paths"]["state"])
        assert state_dir.is_dir()
        assert stat.S_IMODE(manifest.stat().st_mode) == 0o400
        assert stat.S_IMODE(state.stat().st_mode) == 0o600
        combined = json.dumps(payload) + manifest.read_text() + state.read_text()
        assert "M1_SECRET_FIXTURE_123" not in combined
