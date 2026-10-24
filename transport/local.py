from __future__ import annotations
import json, subprocess
from pathlib import Path
from transport.base import ExecRequest
from transport.result import ExecResult

class LocalTransport:
    def __init__(self, runner: Path, runtime: Path): self.runner=runner; self.runtime=runtime
    def exec(self, request: ExecRequest) -> ExecResult:
        p=subprocess.run([str(self.runner),str(self.runtime)],input=json.dumps(request.__dict__),text=True,capture_output=True,check=False)
        if p.returncode not in (0,1): raise RuntimeError(p.stderr or 'runner failed')
        return ExecResult(**json.loads(p.stdout.strip().splitlines()[-1]))
