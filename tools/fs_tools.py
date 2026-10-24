from pathlib import Path
from fsguard.canon import canonical,PathOutsideScope
from fsguard.atomic import atomic_write,StaleFile
from fsguard.safeio import open_read
from tools.envelope import ok,error

def read_file(workspace:Path,path:str,max_bytes=1024*1024):
 try:
  with open_read(path,workspace) as f:data=f.read(max_bytes+1)
  if len(data)>max_bytes:return error('ERR_TOO_LARGE','file exceeds read limit')
  if b'\0' in data[:8192]:return error('ERR_BINARY_FILE','binary file refused')
  return ok({'content':data.decode(),'bytes':len(data)})
 except (PathOutsideScope,OSError) as e:return error('ERR_PATH_OUTSIDE_SCOPE',str(e))
def write_file(workspace:Path,path:str,content:str,expected_sha256=None,create_only=False):
 try:
  target=canonical(path,workspace)
  if create_only and target.exists():return error('ERR_STALE_FILE','target exists')
  digest=atomic_write(target,content.encode(),expected_sha256);return ok({'sha256':digest,'bytes':len(content.encode())})
 except PathOutsideScope as e:return error('ERR_PATH_OUTSIDE_SCOPE',str(e))
 except StaleFile as e:return error('ERR_STALE_FILE',str(e))
def list_dir(workspace:Path,path='.',max_entries=500):
 try:p=canonical(path,workspace);items=sorted(x.name for x in p.iterdir());return ok({'entries':items[:max_entries],'truncated':len(items)>max_entries})
 except Exception as e:return error('ERR_PATH_OUTSIDE_SCOPE',str(e))
