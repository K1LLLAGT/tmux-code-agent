from tmuxctl.server import clean_env
def test_clean_env_excludes_secret(monkeypatch):
 monkeypatch.setenv('API_TOKEN','SECRET');env=clean_env();assert 'API_TOKEN' not in env;assert 'PATH' in env
