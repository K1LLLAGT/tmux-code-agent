from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class ExecResult:
    command_id: str
    argv: list[str]
    cwd: str
    exit_code: int | None
    signal: int | None
    timed_out: bool
    truncated: bool
    stdout_head: str
    stdout_tail: str
    stderr_head: str
    stderr_tail: str
    stdout_bytes: int
    stderr_bytes: int
    log_path: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
