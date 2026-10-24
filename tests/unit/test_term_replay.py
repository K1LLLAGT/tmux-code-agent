from termbridge.replay import ReplayBuffer
def test_replay_cap():
 r=ReplayBuffer(5);r.append(b'abc');r.append(b'def');assert r.bytes()==b'bcdef'
