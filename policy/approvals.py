import hashlib,json,secrets,time
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Approval:
 id:str;binding_hash:str;operation:str;cwd:str;expires_at:float

def binding(tool:str,args:dict,cwd:str)->str:
 raw=json.dumps([tool,args,cwd],sort_keys=True,separators=(',',':')).encode();return hashlib.sha256(raw).hexdigest()
def request(tool:str,args:dict,cwd:str,ttl=600)->Approval:return Approval('ap_'+secrets.token_hex(8),binding(tool,args,cwd),tool,cwd,time.time()+ttl)
def valid(a:Approval,tool:str,args:dict,cwd:str)->bool:return time.time()<=a.expires_at and a.binding_hash==binding(tool,args,cwd)
