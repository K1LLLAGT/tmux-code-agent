from dataclasses import dataclass
from tools.schema import validate
@dataclass(frozen=True,slots=True)
class Tool:
 name:str;spec:dict;handler:object
class Registry:
 def __init__(self):self._tools={}
 def register(self,t:Tool):self._tools[t.name]=t
 def dispatch(self,name,args):
  t=self._tools[name];validate(t.spec,args);return t.handler(**args)
