from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from tmuxctl.server import run
@dataclass(frozen=True,slots=True)
class Pane:
 pane_id:str;window_id:str;window_name:str;active:bool;dead:bool;width:int;height:int

def list_panes(socket:Path)->list[Pane]:
 fmt='#{pane_id}\t#{window_id}\t#{window_name}\t#{pane_active}\t#{pane_dead}\t#{pane_width}\t#{pane_height}'
 p=run(socket,'list-panes','-a','-F',fmt)
 result=[]
 for line in p.stdout.splitlines():
  a=line.split('\t');result.append(Pane(a[0],a[1],a[2],a[3]=='1',a[4]=='1',int(a[5]),int(a[6])))
 return result
def registry(socket:Path)->dict[str,dict]:return {p.pane_id:{'window_id':p.window_id,'window_name':p.window_name,'active':p.active,'dead':p.dead,'width':p.width,'height':p.height} for p in list_panes(socket)}
