from __future__ import annotations
import asyncio,json
from pathlib import Path
async def handle(reader:asyncio.StreamReader,writer:asyncio.StreamWriter)->None:
 line=await reader.readline(); cmd=json.loads(line or b'{}').get('command'); response={'ok':cmd in {'ping','stop'},'command':cmd}
 writer.write((json.dumps(response)+'\n').encode()); await writer.drain(); writer.close(); await writer.wait_closed()
async def start_control(path:Path):
 path.unlink(missing_ok=True); server=await asyncio.start_unix_server(handle,path=str(path)); path.chmod(0o600); return server
