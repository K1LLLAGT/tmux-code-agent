from __future__ import annotations
import json, os, signal, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HEAD_TAIL=4096

def now(): return datetime.now(timezone.utc).isoformat()
def slice_log(path:Path):
    data=path.read_bytes() if path.exists() else b''
    return data[:HEAD_TAIL].decode(errors='replace'),data[-HEAD_TAIL:].decode(errors='replace'),len(data)

def valid_cwd(cwd:Path, workspace:Path)->bool:
    try:cwd=cwd.resolve(strict=True);workspace=workspace.resolve(strict=True)
    except OSError:return False
    return cwd==workspace or workspace in cwd.parents

def run(runtime:Path)->int:
    request=json.loads(sys.stdin.readline())
    if request.get('v',1)!=1: raise SystemExit('bad version')
    expected=(runtime/'session.nonce').read_text().strip()
    if request.get('nonce')!=expected: raise SystemExit('bad nonce')
    workspace=Path((runtime/'workspace').read_text().strip())
    cwd=Path(request['cwd'])
    if not valid_cwd(cwd,workspace): raise SystemExit('bad cwd')
    log_dir=Path(request['log_dir']);log_dir.mkdir(parents=True,exist_ok=True);log_dir.chmod(0o700)
    stdout=log_dir/'stdout.log';stderr=log_dir/'stderr.log';pidfile=log_dir/'pid';result_path=log_dir/'result.json'
    started=now();timed_out=False;sig=None
    with stdout.open('wb') as out, stderr.open('wb') as err:
        p=subprocess.Popen(request['argv'],cwd=cwd,env=request.get('env') or {},stdin=subprocess.PIPE if request.get('stdin') is not None else subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True,text=True)
        pidfile.write_text(str(p.pid));pidfile.chmod(0o600)
        if request.get('stdin') is not None:p.stdin.write(request['stdin']);p.stdin.close()
        try:rc=p.wait(timeout=float(request['timeout_s']))
        except subprocess.TimeoutExpired:
            timed_out=True
            for s,wait in ((signal.SIGINT,float(request['grace_s'])),(signal.SIGTERM,float(request['grace_s'])),(signal.SIGKILL,1.0)):
                try:os.killpg(p.pid,s)
                except ProcessLookupError:break
                try:rc=p.wait(timeout=wait);break
                except subprocess.TimeoutExpired:continue
            else:rc=p.wait()
    if rc<0:sig=-rc;exit_code=None
    else:exit_code=rc
    maxb=int(request['max_output_bytes'])
    for path in (stdout,stderr):
        if path.stat().st_size>maxb:
            data=path.read_bytes();path.write_bytes(data[:maxb//2]+data[-maxb//2:])
    oh,ot,ob=slice_log(stdout);eh,et,eb=slice_log(stderr);truncated=ob>=maxb or eb>=maxb
    result={'command_id':request['command_id'],'argv':request['argv'],'cwd':str(cwd),'exit_code':exit_code,'signal':sig,'timed_out':timed_out,'truncated':truncated,'stdout_head':oh,'stdout_tail':ot,'stderr_head':eh,'stderr_tail':et,'stdout_bytes':ob,'stderr_bytes':eb,'log_path':str(log_dir)}
    result_path.write_text(json.dumps(result,sort_keys=True)+'\n');result_path.chmod(0o600);print(json.dumps(result,separators=(',',':')));return 0 if exit_code==0 and not timed_out else 1

def cancel(command_dir:Path)->int:
    try:pid=int((command_dir/'pid').read_text())
    except Exception:return 1
    try:os.killpg(pid,signal.SIGINT);return 0
    except ProcessLookupError:return 1

def main():
    if len(sys.argv)>=3 and sys.argv[1]=='--cancel':raise SystemExit(cancel(Path(sys.argv[2])))
    if len(sys.argv)>=2 and sys.argv[1]=='--ping':print('{"ok":true}');return
    if len(sys.argv)!=2:raise SystemExit('usage: tca-runner <runtime>')
    raise SystemExit(run(Path(sys.argv[1])))
if __name__=='__main__':main()
