import pytest
from fsguard.canon import canonical,PathOutsideScope
def test_traversal_table(tmp_path):
 root=tmp_path/'w';root.mkdir()
 for value in ('../x','../../etc/passwd','/etc/passwd','x/../../../y','bad\x00x'):
  with pytest.raises(PathOutsideScope):canonical(value,root)
