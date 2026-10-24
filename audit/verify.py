import hashlib,json
from pathlib import Path
def verify(path:Path):
 prev='sha256:'+'0'*64
 for raw in path.read_bytes().splitlines(keepends=True):
  try:e=json.loads(raw)
  except Exception:return False
  if e.get('prev')!=prev:return False
  prev='sha256:'+hashlib.sha256(raw).hexdigest()
 return True
