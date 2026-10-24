#!/data/data/com.termux/files/usr/bin/python
import datetime,json,os,platform,subprocess

def env():
    def out(*a):
        try:return subprocess.check_output(a,text=True,stderr=subprocess.STDOUT,timeout=5).strip()
        except Exception:return None
    return {"prefix":os.getenv("PREFIX"),"python":platform.python_version(),"platform":platform.platform(),"arch":out("uname","-m"),"android_sdk":out("getprop","ro.build.version.sdk")}
def emit(question,spike,status,code,summary,evidence=None):
    print(json.dumps({"schema_version":1,"question":question,"spike":spike,"status":status,"code":code,"summary":summary,"evidence":evidence or {},"environment":env(),"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()},separators=(",",":")))
def termux(): return bool(os.getenv("PREFIX")) and os.path.exists(os.path.join(os.environ["PREFIX"],"bin","pkg"))
def run(argv,timeout=10,env=None):
    p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout,env=env)
    return {"argv":argv,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}
