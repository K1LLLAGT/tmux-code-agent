import hashlib,os,secrets
from pathlib import Path
class StaleFile(ValueError):pass
def sha256(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic_write(path:Path,data:bytes,expected_sha256:str|None=None)->str:
 path.parent.mkdir(parents=True,exist_ok=True)
 if expected_sha256 is not None:
  if not path.exists() or sha256(path)!=expected_sha256:raise StaleFile('ERR_STALE_FILE')
 tmp=path.parent/f'.tca-tmp-{secrets.token_hex(6)}';fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,path)
  try:d=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(d);os.close(d)
  except OSError:pass
 finally:
  tmp.unlink(missing_ok=True)
 return sha256(path)
