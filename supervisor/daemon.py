from __future__ import annotations
import argparse,asyncio,os,signal
from pathlib import Path
import uvicorn
from supervisor.control import start_control
from supervisor.heartbeat import write_heartbeat
from supervisor.lock import acquire_lock,release_lock
from web.app import create_app
async def run(runtime:Path,port:int)->None:
 runtime.mkdir(parents=True,exist_ok=True); runtime.chmod(0o700); lock=runtime/'daemon.lock'; acquire_lock(lock); ctl=await start_control(runtime/'ctl.sock'); hb=runtime/'heartbeat'; stop=asyncio.Event()
 loop=asyncio.get_running_loop()
 for sig in (signal.SIGTERM,signal.SIGINT):
  try:loop.add_signal_handler(sig,stop.set)
  except NotImplementedError:pass
 config=uvicorn.Config(create_app(),host='127.0.0.1',port=port,log_level='warning'); server=uvicorn.Server(config); task=asyncio.create_task(server.serve())
 try:
  while not stop.is_set():write_heartbeat(hb); await asyncio.sleep(.5)
 finally:
  server.should_exit=True; await task; ctl.close(); await ctl.wait_closed(); release_lock(lock)
def main():
 p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--port',type=int,required=True);a=p.parse_args();asyncio.run(run(a.runtime,a.port))
if __name__=='__main__':main()
