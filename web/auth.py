from __future__ import annotations
import hmac,secrets
from dataclasses import dataclass,field
@dataclass(slots=True)
class AuthState:
 bootstrap_token:str=field(default_factory=lambda:secrets.token_urlsafe(32)); sessions:dict[str,str]=field(default_factory=dict)
 def claim(self,token:str)->tuple[str,str]|None:
  if not hmac.compare_digest(token,self.bootstrap_token): return None
  sid=secrets.token_urlsafe(32); csrf=secrets.token_urlsafe(32); self.sessions[sid]=csrf; self.bootstrap_token=secrets.token_urlsafe(32); return sid,csrf
 def csrf(self,sid:str|None)->str|None:return self.sessions.get(sid or '')
