#!/data/data/com.termux/files/usr/bin/python
from common import *
import os,tempfile,hashlib
if not termux(): emit('Q10','filesystem-semantics','SKIP','NOT_TERMUX','Target Termux required');raise SystemExit(2)
def test(root):
 os.makedirs(root,exist_ok=True);d=tempfile.mkdtemp(prefix='tca-',dir=root);ev={'root':root,'supports_dir_fd':os.open in os.supports_dir_fd,'O_NOFOLLOW':hasattr(os,'O_NOFOLLOW')}
 try:
  dfd=os.open(d,os.O_RDONLY|getattr(os,'O_DIRECTORY',0));fd=os.open('a.tmp',os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600,dir_fd=dfd);os.write(fd,b'tca');os.fsync(fd);os.close(fd);os.replace('a.tmp','a',src_dir_fd=dfd,dst_dir_fd=dfd);ev['sha256']=hashlib.sha256(open(d+'/a','rb').read()).hexdigest();os.unlink('a',dir_fd=dfd);os.close(dfd);ev['ok']=True
 except Exception as e:ev['ok']=False;ev['error']=repr(e)
 finally:
  try:os.rmdir(d)
  except:pass
 return ev
ev={'private':test(os.path.join(os.environ['HOME'],'.cache'))};shared=os.path.expanduser('~/storage/shared');ev['shared']=test(shared) if os.path.isdir(shared) else {'skipped':'termux-setup-storage not available'};ok=ev['private'].get('ok',False)
emit('Q10','filesystem-semantics','PASS' if ok else 'FAIL','PRIVATE_STORAGE_OK' if ok else 'PRIVATE_STORAGE_FAILED','Private and available shared-storage semantics were measured separately',ev);raise SystemExit(0 if ok else 1)
