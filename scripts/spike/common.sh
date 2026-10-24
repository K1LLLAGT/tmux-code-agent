#!/data/data/com.termux/files/usr/bin/bash
set -u
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
emit(){ python -c 'import datetime,json,os,platform,sys;q,n,s,c,m,e=sys.argv[1:];print(json.dumps({"schema_version":1,"question":q,"spike":n,"status":s,"code":c,"summary":m,"evidence":{"text":e},"environment":{"prefix":os.getenv("PREFIX"),"python":platform.python_version(),"platform":platform.platform()},"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat()},separators=(",",":")))' "$@"; }
is_termux(){ [ -n "${PREFIX:-}" ] && [ -x "$PREFIX/bin/pkg" ]; }
