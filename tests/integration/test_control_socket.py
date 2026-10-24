import asyncio,json
from supervisor.control import start_control
def test_control(tmp_path):
 async def go():
  p=tmp_path/'ctl.sock';s=await start_control(p);r,w=await asyncio.open_unix_connection(str(p));w.write(b'{"command":"ping"}\n');await w.drain();data=json.loads(await r.readline());assert data['ok'];w.close();await w.wait_closed();s.close();await s.wait_closed()
 asyncio.run(go())
