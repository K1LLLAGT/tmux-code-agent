from __future__ import annotations
from termbridge.frames import parse_frame
class BackpressureGate:
 def __init__(self,high=256*1024,low=128*1024):self.high=high;self.low=low;self.paused=False
 def update(self,pending:int)->bool:
  if not self.paused and pending>=self.high:self.paused=True
  elif self.paused and pending<=self.low:self.paused=False
  return self.paused

def handle_client_frame(frame:bytes,pty):
 kind,payload=parse_frame(frame)
 if kind=='data':pty.write(payload);return 'data'
 if payload.get('type')=='resize':pty.resize(int(payload['cols']),int(payload['rows']));return 'resize'
 if payload.get('type')=='ping':return 'ping'
 raise ValueError('unsupported terminal control')
