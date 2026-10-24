import asyncio
from models.base import Chunk
from agent.engine import AgentEngine
class P:
 def __init__(self):self.i=0
 async def stream(self,req):
  self.i+=1
  if self.i==1:yield Chunk(tool_call={'tool':'echo','args':{'value':'x'}})
  else:yield Chunk(tool_call={'tool':'finish','args':{'summary':'ok','claims':[]}})
def test_scripted_agent():
 seen=[]
 def dispatch(n,a):seen.append((n,a));return {'ok':True,'data':a}
 r=asyncio.run(AgentEngine(P(),dispatch).run('task','tree'));assert r['ok'] and seen==[('echo',{'value':'x'})]
