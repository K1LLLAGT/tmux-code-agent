from __future__ import annotations
from collections import deque
class EventRing:
 def __init__(self,max_events=2000):self.events=deque(maxlen=max_events);self.seq=0
 def publish(self,type_,data):
  self.seq+=1;e={'seq':self.seq,'type':type_,'data':data};self.events.append(e);return e
 def replay(self,last_seq:int):return [e for e in self.events if e['seq']>last_seq]
