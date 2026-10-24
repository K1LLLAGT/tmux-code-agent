import os
from pathlib import Path
def move_to_trash(path:Path,workspace:Path,trash_root:Path)->Path:
 rel=path.resolve().relative_to(workspace.resolve());dest=trash_root/rel;dest.parent.mkdir(parents=True,exist_ok=True);os.replace(path,dest);return dest
