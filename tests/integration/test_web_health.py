from starlette.testclient import TestClient
from web.app import create_app
def test_health():
 with TestClient(create_app()) as c:
  r=c.get('/health',headers={'host':'127.0.0.1'});assert r.status_code==200 and r.json()['ok'] is True
