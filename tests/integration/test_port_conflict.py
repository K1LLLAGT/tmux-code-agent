import socket
from supervisor.ports import reserve_loopback_port
def test_reserved_port_conflicts():
 s,p=reserve_loopback_port();other=socket.socket();
 try:
  try:other.bind(('127.0.0.1',p));ok=True
  except OSError:ok=False
  assert ok is False
 finally:other.close();s.close()
