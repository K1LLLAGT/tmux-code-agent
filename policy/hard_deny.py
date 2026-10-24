from pathlib import Path
DENIED_GIT=(('git','reset','--hard'),('git','clean','-fd'),('git','clean','-fdx'),('git','checkout','--'),('git','stash','drop'),('git','stash','clear'))
def command_denied(argv:list[str])->bool:
 t=tuple(argv)
 return any(t[:len(x)]==x for x in DENIED_GIT) or (len(t)>=2 and t[0]=='git' and t[1].startswith('push') and any(a.startswith('--force') for a in t))
def protected_write(path:Path,state:Path,runtime:Path,home:Path,prefix:Path)->bool:
 p=path.resolve(strict=False)
 for root in (state.resolve(),runtime.resolve(),(home/'.ssh').resolve(),(prefix/'etc').resolve()):
  if p==root or root in p.parents:return True
 return '.git' in p.parts
