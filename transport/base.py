from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from transport.result import ExecResult

@dataclass(frozen=True, slots=True)
class ExecRequest:
    command_id: str
    argv: list[str]
    cwd: str
    env: dict[str, str]
    timeout_s: float
    grace_s: float
    max_output_bytes: int
    log_dir: str
    nonce: str
    stdin: str | None = None

class Transport(Protocol):
    def exec(self, request: ExecRequest) -> ExecResult: ...
