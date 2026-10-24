from __future__ import annotations
import itertools,subprocess
from pathlib import Path
_counter=itertools.count(1)
def create_viewer(socket:Path,window:str='user')->str:
 name=f'view-{next(_counter)}';subprocess.run(['tmux','-S',str(socket),'new-session','-d','-t','tca','-s',name],check=True);subprocess.run(['tmux','-S',str(socket),'select-window','-t',f'{name}:{window}'],check=True);return name
def destroy_viewer(socket:Path,name:str)->None:subprocess.run(['tmux','-S',str(socket),'kill-session','-t',name],check=False)
