from __future__ import annotations
import subprocess,time
from pathlib import Path

def start_sshd(config:Path)->subprocess.Popen[str]:
    exe=subprocess.check_output(['command','-v','sshd'],text=True,shell=True).strip()
    p=subprocess.Popen([exe,'-D','-e','-f',str(config)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
    time.sleep(.15)
    if p.poll() is not None: raise RuntimeError((p.stderr.read() if p.stderr else '') or 'sshd failed')
    return p

def stop_sshd(p:subprocess.Popen[str])->None:
    if p.poll() is None:
        p.terminate()
        try:p.wait(timeout=3)
        except subprocess.TimeoutExpired:p.kill();p.wait(timeout=3)
