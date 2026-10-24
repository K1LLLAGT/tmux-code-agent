from __future__ import annotations
import json, os, subprocess
from pathlib import Path
from transport.base import ExecRequest
from transport.result import ExecResult

class SshTransport:
    def __init__(self, *, port:int, key:Path, known_hosts:Path, control_path:Path):
        self.port=port; self.key=key; self.known_hosts=known_hosts; self.control_path=control_path
    def argv(self) -> list[str]:
        return ['ssh','-F','none','-p',str(self.port),'-i',str(self.key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={self.known_hosts}','-o','ControlMaster=auto','-o','ControlPersist=60','-o',f'ControlPath={self.control_path}','-o','ServerAliveInterval=10','-o','ServerAliveCountMax=3','-o','LogLevel=ERROR','127.0.0.1']
    def exec(self, request:ExecRequest)->ExecResult:
        p=subprocess.run(self.argv(),input=json.dumps(request.__dict__),text=True,capture_output=True,check=False)
        if not p.stdout.strip(): raise RuntimeError(p.stderr or 'ssh transport failed')
        return ExecResult(**json.loads(p.stdout.strip().splitlines()[-1]))
