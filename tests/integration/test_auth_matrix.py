from starlette.testclient import TestClient
from web.app import create_app
def test_auth_matrix():
 app=create_app()
 with TestClient(app) as c:
  assert c.get('/health',headers={'host':'evil.example'}).status_code==400
  assert c.get('/health',headers={'host':'127.0.0.1','origin':'https://evil.example'}).status_code==403
  token=app.state.auth.bootstrap_token
  r=c.post('/bootstrap/claim',json={'token':token},headers={'host':'127.0.0.1'});assert r.status_code==200 and r.cookies.get('tca_session')
  csrf=r.json()['csrf'];assert c.post('/api/state',headers={'host':'127.0.0.1'}).status_code in {403,405}
