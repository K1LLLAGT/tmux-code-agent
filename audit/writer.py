import hashlib,json,os
from pathlib import Path
class AuditWriter:
 def __init__(self,path:Path,session='test'):self.path=path;self.session=session;self.seq=0;self.prev='sha256:'+'0'*64
 def append(self,type_,data,actor='system'):
  self.seq+=1;e={'v':1,'seq':self.seq,'session':self.session,'actor':actor,'type':type_,'data':data,'prev':self.prev};line=json.dumps(e,sort_keys=True,separators=(',',':'))+'\n';self.path.parent.mkdir(parents=True,exist_ok=True);fd=os.open(self.path,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600);os.write(fd,line.encode());os.close(fd);self.prev='sha256:'+hashlib.sha256(line.encode()).hexdigest();return e
