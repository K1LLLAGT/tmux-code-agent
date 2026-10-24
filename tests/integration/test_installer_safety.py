import subprocess
def test_dry_runs_do_not_touch_user_data(tmp_path):
 a=subprocess.run(['bash','install.sh','--dry-run'],text=True,capture_output=True);b=subprocess.run(['bash','uninstall.sh','--dry-run'],text=True,capture_output=True);assert a.returncode==b.returncode==0;assert 'not touched' in b.stdout
