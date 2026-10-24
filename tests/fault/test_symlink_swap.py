import pytest
from fsguard.safeio import open_read
def test_final_symlink_blocked(tmp_path):
 w=tmp_path/'w';w.mkdir();inside=w/'a';inside.write_text('ok');outside=tmp_path/'o';outside.write_text('no');inside.unlink();inside.symlink_to(outside)
 with pytest.raises(Exception):open_read('a',w)
