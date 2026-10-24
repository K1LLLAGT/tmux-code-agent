from __future__ import annotations
import os, subprocess
from pathlib import Path

def generate_ed25519(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(path)], check=True)
    os.chmod(path, 0o600)
    os.chmod(Path(str(path)+'.pub'), 0o600)

def generate_session_keys(ssh_dir: Path) -> dict[str, Path]:
    ssh_dir.mkdir(parents=True, exist_ok=True)
    ssh_dir.chmod(0o700)
    host=ssh_dir/'host_ed25519'; exec_key=ssh_dir/'exec_ed25519'; pty_key=ssh_dir/'pty_ed25519'
    for p in (host,exec_key,pty_key):
        if not p.exists(): generate_ed25519(p)
    return {'host':host,'exec':exec_key,'pty':pty_key}
