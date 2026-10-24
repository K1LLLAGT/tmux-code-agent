from __future__ import annotations
import os,subprocess
from pathlib import Path
from tmuxctl.conf import write_config

def _base(socket:Path)->list[str]:return ['tmux','-S',str(socket)]
def clean_env(extra:dict[str,str]|None=None)->dict[str,str]:
 env={'HOME':os.environ['HOME'],'PREFIX':os.environ['PREFIX'],'PATH':os.environ['PATH'],'TERM':os.environ.get('TERM','xterm-256color'),'LANG':os.environ.get('LANG','C.UTF-8')}
 if extra:env.update(extra)
 return env

def run(socket:Path,*args:str,check=True,env=None):return subprocess.run([*_base(socket),*args],text=True,capture_output=True,check=check,env=env or clean_env())
def server_alive(socket:Path)->bool:return run(socket,'has-session',check=False).returncode==0
def start_private_server(socket:Path,workspace:Path,shell:str|None=None)->None:
 socket.parent.mkdir(parents=True,exist_ok=True);socket.parent.chmod(0o700);conf=write_config(socket.parent/'tmux.conf');sh=shell or os.environ.get('SHELL') or f"{os.environ['PREFIX']}/bin/sh"
 if server_alive(socket):return
 subprocess.run([*_base(socket),'-f',str(conf),'new-session','-d','-s','tca','-n','user','-c',str(workspace),sh],check=True,env=clean_env())
 for name in ('agent','logs'):run(socket,'new-window','-d','-t','tca:','-n',name,'-c',str(workspace),sh)
def kill_server(socket:Path)->None:run(socket,'kill-server',check=False)
def adopt(socket:Path)->bool:return server_alive(socket)
