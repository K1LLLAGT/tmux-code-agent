from supervisor.ports import reserve_loopback_port
def test_port():
 s,p=reserve_loopback_port();assert p>0;assert s.getsockname()[0]=='127.0.0.1';s.close()
