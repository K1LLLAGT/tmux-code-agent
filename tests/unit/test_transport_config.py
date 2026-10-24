from pathlib import Path
from transport.config import authorized_keys
def test_authorized_keys():
 t=authorized_keys('ssh-ed25519 AAA exec','ssh-ed25519 BBB pty',Path('/r/tca-runner'),Path('/rt'));assert 'restrict,command=' in t and 'restrict,pty' in t
