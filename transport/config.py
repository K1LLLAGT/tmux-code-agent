from __future__ import annotations
import os, shlex
from pathlib import Path

def authorized_keys(exec_pub: str, pty_pub: str, runner: Path, runtime: Path) -> str:
    forced=f'{shlex.quote(str(runner))} {shlex.quote(str(runtime))}'
    return (
        f'restrict,command="{forced}" {exec_pub.strip()}\n'
        f'restrict,pty {pty_pub.strip()}\n'
    )

def write_sshd_config(path: Path, *, port: int, runtime: Path, host_key: Path, authorized: Path) -> Path:
    text=f'''Port {port}\nListenAddress 127.0.0.1\nHostKey {host_key}\nPidFile {runtime}/ssh/sshd.pid\nAuthorizedKeysFile {authorized}\nPubkeyAuthentication yes\nStrictModes no\nPasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin no\nAllowTcpForwarding no\nAllowStreamLocalForwarding no\nAllowAgentForwarding no\nX11Forwarding no\nPermitTunnel no\nGatewayPorts no\nPermitUserEnvironment no\nPermitUserRC no\nPrintMotd no\nMaxSessions 16\nMaxAuthTries 2\nLoginGraceTime 10\nClientAliveInterval 15\nClientAliveCountMax 3\nLogLevel ERROR\n'''
    path.write_text(text); os.chmod(path,0o600); return path

