import os
from pathlib import Path
from fsguard.canon import canonical
class UnsafePath(ValueError):pass
def _parts(target:Path,root:Path):return target.relative_to(root).parts
def open_read(path,root:Path):
 root=root.resolve(strict=True);target=canonical(path,root);fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY)
 try:
  parts=_parts(target,root)
  for i,name in enumerate(parts):
   flags=os.O_RDONLY|os.O_NOFOLLOW
   if i<len(parts)-1:flags|=os.O_DIRECTORY
   new=os.open(name,flags,dir_fd=fd);os.close(fd);fd=new
  return os.fdopen(fd,'rb')
 except Exception:
  os.close(fd);raise
