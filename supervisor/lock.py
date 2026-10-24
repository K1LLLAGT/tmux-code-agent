from __future__ import annotations
import json, os
from pathlib import Path
from core.errors import StateError

def pid_alive(pid:int)->bool:
 if pid<=0:return False
 try: os.kill(pid,0); return True
 except ProcessLookupError:return False
 except PermissionError:return True

def read_pid(path:Path)->int|None:
 try:return int(json.loads(path.read_text())["pid"])
 except (FileNotFoundError,ValueError,KeyError,json.JSONDecodeError,TypeError):return None

def acquire_lock(path:Path,pid:int|None=None)->int:
 current=read_pid(path)
 if current and pid_alive(current): raise StateError("daemon already running",code="ERR_DAEMON_RUNNING")
 path.parent.mkdir(parents=True,exist_ok=True)
 me=os.getpid() if pid is None else pid
 path.write_text(json.dumps({"pid":me})+"\n"); os.chmod(path,0o600); return me

def release_lock(path:Path,pid:int|None=None)->None:
 expected=os.getpid() if pid is None else pid
 if read_pid(path)==expected:path.unlink(missing_ok=True)
