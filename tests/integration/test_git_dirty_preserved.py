import subprocess
from gitsafe.run import git
def test_dirty_preserved(tmp_path):
 w=tmp_path/'r';w.mkdir();subprocess.run(['git','init','-q',str(w)],check=True);subprocess.run(['git','-C',str(w),'config','user.email','a@b'],check=True);subprocess.run(['git','-C',str(w),'config','user.name','T'],check=True);(w/'a').write_text('base\n');subprocess.run(['git','-C',str(w),'add','a'],check=True);subprocess.run(['git','-C',str(w),'commit','-qm','i'],check=True);(w/'a').write_text('user\n');before=(w/'a').read_bytes();git(w,'status','--porcelain=v2');assert (w/'a').read_bytes()==before
