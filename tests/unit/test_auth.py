from web.auth import AuthState
def test_claim_is_one_time():
 a=AuthState();t=a.bootstrap_token;r=a.claim(t);assert r and a.claim(t) is None;assert a.csrf(r[0])==r[1]
