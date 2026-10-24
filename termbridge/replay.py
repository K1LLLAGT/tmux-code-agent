from __future__ import annotations
from collections import deque
class ReplayBuffer:
 def __init__(self,max_bytes=512*1024):self.max_bytes=max_bytes;self._chunks=deque();self._size=0
 def append(self,data:bytes):
  if not data:return
  self._chunks.append(data);self._size+=len(data)
  while self._size>self.max_bytes and self._chunks:
   excess=self._size-self.max_bytes;first=self._chunks[0]
   if len(first)<=excess:self._chunks.popleft();self._size-=len(first)
   else:self._chunks[0]=first[excess:];self._size-=excess
 def bytes(self)->bytes:return b''.join(self._chunks)
