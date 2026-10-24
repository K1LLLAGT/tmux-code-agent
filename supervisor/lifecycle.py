from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

class SessionStatus(StrEnum):
    CREATED="CREATED"; STARTING="STARTING"; READY="READY"; STOPPING="STOPPING"; STOPPED="STOPPED"; ORPHANED="ORPHANED"; FAILED="FAILED"

_ALLOWED={
 SessionStatus.CREATED:{SessionStatus.STARTING,SessionStatus.FAILED},
 SessionStatus.STARTING:{SessionStatus.READY,SessionStatus.FAILED,SessionStatus.ORPHANED},
 SessionStatus.READY:{SessionStatus.STOPPING,SessionStatus.ORPHANED,SessionStatus.FAILED},
 SessionStatus.STOPPING:{SessionStatus.STOPPED,SessionStatus.FAILED},
 SessionStatus.STOPPED:set(), SessionStatus.ORPHANED:{SessionStatus.STARTING,SessionStatus.STOPPED}, SessionStatus.FAILED:{SessionStatus.STARTING,SessionStatus.STOPPED},
}
@dataclass(slots=True)
class Lifecycle:
 status:SessionStatus=SessionStatus.CREATED
 updated_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
 def transition(self,target:SessionStatus)->None:
  if target not in _ALLOWED[self.status]: raise ValueError(f"invalid transition {self.status}->{target}")
  self.status=target; self.updated_at=datetime.now(timezone.utc).isoformat()
