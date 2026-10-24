import subprocess
from gitsafe.run import git
def test_fsmonitor_disabled(tmp_path):
 w=tmp_path/'r';w.mkdir();subprocess.run(['git','init','-q',str(w)],check=True);marker=tmp_path/'PWN';subprocess.run(['git','-C',str(w),'config','core.fsmonitor',f'touch {marker}'],check=True);git(w,'status',check=False);assert not marker.exists()
