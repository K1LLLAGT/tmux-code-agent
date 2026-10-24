import pytest
from fsguard.atomic import atomic_write,sha256,StaleFile
def test_atomic_and_stale(tmp_path):
 p=tmp_path/'a';h=atomic_write(p,b'one');assert sha256(p)==h;atomic_write(p,b'two',h)
 with pytest.raises(StaleFile):atomic_write(p,b'three',h)
 assert not list(tmp_path.glob('.tca-tmp-*'))
