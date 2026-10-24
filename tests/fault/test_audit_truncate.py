from audit.writer import AuditWriter
from audit.verify import verify
def test_truncate_detected(tmp_path):
 p=tmp_path/'e';w=AuditWriter(p);w.append('a',{});w.append('b',{});p.write_bytes(p.read_bytes()[:-7]);assert not verify(p)
