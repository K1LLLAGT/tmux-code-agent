from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol,AsyncIterator
@dataclass(frozen=True,slots=True)
class ModelInfo:id:str
@dataclass(frozen=True,slots=True)
class Caps:context_tokens:int=4096;tool_mode:str='chat_only';streaming:bool=True;max_output:int=1024
@dataclass(frozen=True,slots=True)
class Health:ok:bool;detail:str=''
@dataclass(frozen=True,slots=True)
class Chunk:text:str='';tool_call:dict|None=None
class ModelProvider(Protocol):
 id:str
 async def discover(self)->list[ModelInfo]:...
 async def capabilities(self,model:str)->Caps:...
 async def health(self)->Health:...
 async def stream(self,request:dict)->AsyncIterator[Chunk]:...
