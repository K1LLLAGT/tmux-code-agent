from __future__ import annotations
import json,urllib.request
from models.base import ModelInfo,Caps,Health,Chunk
class OpenAICompatProvider:
 id='openai_compat'
 def __init__(self,base_url:str,model:str='auto'):self.base_url=base_url.rstrip('/');self.model=model
 def _json(self,path:str,payload=None):
  data=None if payload is None else json.dumps(payload).encode();req=urllib.request.Request(self.base_url+path,data=data,headers={'Content-Type':'application/json'} if data else {});return json.load(urllib.request.urlopen(req,timeout=5))
 async def discover(self):return [ModelInfo(x['id']) for x in self._json('/models').get('data',[])]
 async def capabilities(self,model):return Caps(context_tokens=4096,tool_mode='native_tools')
 async def health(self):
  try:self._json('/models');return Health(True,'reachable')
  except Exception as e:return Health(False,str(e))
 async def stream(self,request):
  payload={'model':self.model if self.model!='auto' else request.get('model','test'),'messages':request['messages'],'tools':request.get('tools',[]),'stream':False};body=self._json('/chat/completions',payload);msg=body['choices'][0]['message'];
  if msg.get('tool_calls'):
   call=msg['tool_calls'][0];yield Chunk(tool_call={'tool':call['function']['name'],'args':json.loads(call['function']['arguments'])})
  elif msg.get('content'):yield Chunk(text=msg['content'])
