"""M1 launch orchestration and dry-run creation path."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from core.config import Config
from core.context import capture_context
from core.ids import new_session_id
from core.manifest import build_manifest, write_manifest
from core.paths import SessionPaths, assert_unix_path, build_session_paths, create_session_dirs
from core.state import initial_state, write_state_atomic


def _override_paths(paths: SessionPaths, config: Config) -> SessionPaths:
    state_root = Path(config.state_root).expanduser() if config.state_root else paths.state_root
    runtime_root = Path(config.runtime_root).expanduser() if config.runtime_root else paths.runtime_root
    overridden = SessionPaths(
        session_id=paths.session_id,
        state_root=state_root,
        state_dir=state_root / paths.session_id,
        runtime_root=runtime_root,
        runtime_dir=runtime_root / paths.runtime_dir.name,
    )
    assert_unix_path(overridden.tmux_socket)
    assert_unix_path(overridden.control_socket)
    return overridden


def dry_run_start(
    *,
    workspace: str | None,
    config: Config,
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    source = dict(os.environ if environ is None else environ)
    context = capture_context(
        logical_pwd=workspace,
        environ=source,
        allow_home=config.allow_home_workspace,
        allow_root=config.allow_root_workspace,
    )
    session_id = new_session_id()
    paths = build_session_paths(session_id, home=context.home, prefix=context.prefix)
    paths = _override_paths(paths, config)
    create_session_dirs(paths)
    manifest = build_manifest(context, paths)
    write_manifest(paths.manifest, manifest)
    state = initial_state(session_id)
    write_state_atomic(paths.state, state)
    return {
        "dry_run": True,
        "session_id": session_id,
        "context": context.as_dict(),
        "manifest": manifest.as_dict(),
        "state": state.as_dict(),
        "config": config.as_dict(),
        "paths": {
            "state_dir": str(paths.state_dir),
            "runtime_dir": str(paths.runtime_dir),
            "manifest": str(paths.manifest),
            "state": str(paths.state),
            "tmux_socket": str(paths.tmux_socket),
            "control_socket": str(paths.control_socket),
        },
    }


def _write_live_state(path: Path, session_id: str, status: str, components: dict[str, str]) -> None:
    """Persist the live lifecycle using the existing atomic state writer."""
    from datetime import datetime, timezone
    from core.state import SessionState

    write_state_atomic(
        path,
        SessionState(
            schema_version=1,
            session_id=session_id,
            status=status,
            updated_at=datetime.now(timezone.utc).isoformat(),
            components=components,
        ),
    )


def live_start(
    *,
    workspace: str | None,
    config: Config,
    environ: dict[str, str] | None = None,
    ready_timeout_s: float = 8.0,
) -> dict[str, Any]:
    """Start one live TCA session and return only after its health gate is READY."""
    import json
    import subprocess
    import sys
    import time
    import urllib.error
    import urllib.request

    from supervisor.ports import reserve_loopback_port
    from tmuxctl.server import kill_server, start_private_server

    source = dict(os.environ if environ is None else environ)
    context = capture_context(
        logical_pwd=workspace,
        environ=source,
        allow_home=config.allow_home_workspace,
        allow_root=config.allow_root_workspace,
    )
    session_id = new_session_id()
    paths = _override_paths(
        build_session_paths(session_id, home=context.home, prefix=context.prefix),
        config,
    )
    create_session_dirs(paths)
    manifest = build_manifest(context, paths)
    write_manifest(paths.manifest, manifest)
    write_state_atomic(paths.state, initial_state(session_id))

    components: dict[str, str] = {
        "tmux": "STARTING",
        "backend": "STARTING",
    }
    _write_live_state(paths.state, session_id, "STARTING", components)

    daemon_log = paths.runtime_dir / "daemon.log"
    daemon_pid_file = paths.runtime_dir / "daemon.pid"
    port_file = paths.runtime_dir / "web.port"
    url_file = paths.runtime_dir / "url"
    daemon: subprocess.Popen[bytes] | None = None

    try:
        start_private_server(paths.tmux_socket, Path(context.workspace))
        components["tmux"] = "READY"
        _write_live_state(paths.state, session_id, "STARTING", components)

        reserve, web_port = reserve_loopback_port()
        reserve.close()
        port_file.write_text(f"{web_port}\n", encoding="utf-8")
        os.chmod(port_file, 0o600)

        with daemon_log.open("ab", buffering=0) as log:
            daemon = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "supervisor.daemon",
                    "--runtime",
                    str(paths.runtime_dir),
                    "--port",
                    str(web_port),
                ],
                cwd=context.workspace,
                env={
                    **source,
                    "PYTHONPATH": str(Path(__file__).resolve().parents[1])
                    + (":" + source["PYTHONPATH"] if source.get("PYTHONPATH") else ""),
                },
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=log,
                start_new_session=True,
            )
        daemon_pid_file.write_text(f"{daemon.pid}\n", encoding="utf-8")
        os.chmod(daemon_pid_file, 0o600)

        health = f"http://127.0.0.1:{web_port}/health"
        deadline = time.monotonic() + ready_timeout_s
        payload: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            if daemon.poll() is not None:
                raise RuntimeError(f"supervisor daemon exited with {daemon.returncode}")
            try:
                with urllib.request.urlopen(health, timeout=0.3) as response:
                    payload = json.load(response)
                if payload.get("ok") is True:
                    break
            except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError("supervisor health gate timed out")

        required = [
            paths.tmux_socket,
            paths.control_socket,
            paths.runtime_dir / "heartbeat",
            paths.runtime_dir / "daemon.lock",
        ]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise RuntimeError("readiness artifacts missing: " + ", ".join(missing))

        url = f"http://127.0.0.1:{web_port}/"
        url_file.write_text(url + "\n", encoding="utf-8")
        os.chmod(url_file, 0o600)
        components["backend"] = "READY"
        _write_live_state(paths.state, session_id, "READY", components)

        return {
            "dry_run": False,
            "session_id": session_id,
            "status": "READY",
            "url": url,
            "web_port": web_port,
            "daemon_pid": daemon.pid,
            "paths": {
                "state_dir": str(paths.state_dir),
                "runtime_dir": str(paths.runtime_dir),
                "manifest": str(paths.manifest),
                "state": str(paths.state),
                "tmux_socket": str(paths.tmux_socket),
                "control_socket": str(paths.control_socket),
                "daemon_log": str(daemon_log),
            },
        }
    except Exception:
        components["backend"] = "FAILED"
        _write_live_state(paths.state, session_id, "FAILED", components)
        if daemon is not None and daemon.poll() is None:
            daemon.terminate()
            try:
                daemon.wait(timeout=3)
            except subprocess.TimeoutExpired:
                daemon.kill()
                daemon.wait(timeout=3)
        kill_server(paths.tmux_socket)
        raise
