import pytest
from fsguard.safeio import open_read
def test_symlink_escape_refused(tmp_path):
 root=tmp_path/'w';root.mkdir();outside=tmp_path/'secret';outside.write_text('secret');(root/'link').symlink_to(outside)
 with pytest.raises(Exception):open_read('link',root)
