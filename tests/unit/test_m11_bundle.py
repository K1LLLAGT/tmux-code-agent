import pytest
from audit.bundle import safe_bundle
def test_bundle_fails_closed(tmp_path):
 p=tmp_path/'x';p.write_text('-----BEGIN PRIVATE KEY-----')
 with pytest.raises(ValueError):safe_bundle([p],tmp_path/'b.tgz')
