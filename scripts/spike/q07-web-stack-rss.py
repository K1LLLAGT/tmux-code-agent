#!/data/data/com.termux/files/usr/bin/python
import datetime,json,os,platform,resource,socket,subprocess,tempfile,time,urllib.request
from pathlib import Path

def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1',0)); return s.getsockname()[1]

def rss_kib(pid):
    p=Path(f'/proc/{pid}/status')
    if p.exists():
        for line in p.read_text(errors='replace').splitlines():
            if line.startswith('VmRSS:'): return int(line.split()[1])
    return None

def emit(status,code,summary,evidence,rc):
    print(json.dumps({'schema_version':1,'question':'Q07','spike':'live-starlette-uvicorn-rss','status':status,'code':code,'summary':summary,'evidence':evidence,'environment':{'prefix':os.getenv('PREFIX'),'python':platform.python_version(),'platform':platform.platform(),'arch':platform.machine()},'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()},separators=(',',':')));raise SystemExit(rc)

try:
    import starlette,uvicorn,websockets,h11,anyio
except Exception as e: emit('FAIL','IMPORT_FAILED','Candidate stack import failed',{'error':repr(e)},1)
port=free_port(); proc=None
with tempfile.TemporaryDirectory(prefix='tca-q07-',dir=os.getenv('TMPDIR')) as td:
    d=Path(td); app=d/'app.py'; out=d/'stdout.log'; err=d/'stderr.log'
    app.write_text("from starlette.applications import Starlette\nfrom starlette.responses import JSONResponse\nfrom starlette.routing import Route\nasync def health(request): return JSONResponse({'status':'ok'})\napp=Starlette(routes=[Route('/health',health)])\n")
    cmd=[os.sys.executable,'-m','uvicorn','app:app','--app-dir',str(d),'--host','127.0.0.1','--port',str(port),'--workers','1','--log-level','warning','--no-access-log']
    with out.open('w') as so, err.open('w') as se:
        proc=subprocess.Popen(cmd,stdout=so,stderr=se,text=True)
    try:
        responses=[]; deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if proc.poll() is not None: break
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=.5) as r:
                    body=r.read().decode(); responses.append({'status':r.status,'body':body}); break
            except Exception: time.sleep(.1)
        if not responses:
            emit('FAIL','SERVER_NOT_READY','Uvicorn health endpoint did not become ready',{'command':cmd,'returncode':proc.poll(),'stderr':err.read_text(errors='replace')[-8000:]},1)
        samples=[]
        for _ in range(10):
            samples.append(rss_kib(proc.pid)); time.sleep(.2)
        for _ in range(20):
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=2) as r: responses.append({'status':r.status,'body':r.read().decode()})
        after=rss_kib(proc.pid)
        valid=[x for x in samples if x is not None]
        evidence={'command':cmd,'pid':proc.pid,'bind_host':'127.0.0.1','port':port,'versions':{'starlette':starlette.__version__,'uvicorn':uvicorn.__version__,'websockets':websockets.__version__,'h11':h11.__version__,'anyio':getattr(anyio,'__version__',None)},'health_requests':len(responses),'all_health_200':all(x['status']==200 and '"status":"ok"' in x['body'].replace(' ','') for x in responses),'idle_rss_samples_kib':samples,'idle_rss_min_kib':min(valid) if valid else None,'idle_rss_max_kib':max(valid) if valid else None,'rss_after_requests_kib':after,'probe_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        ok=evidence['all_health_200'] and bool(valid)
        emit('PASS' if ok else 'FAIL','LIVE_WEB_STACK_OK' if ok else 'LIVE_WEB_STACK_FAILED','Live Starlette/Uvicorn health and RSS measurement completed',evidence,0 if ok else 1)
    finally:
        if proc and proc.poll() is None:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill();proc.wait(timeout=2)
