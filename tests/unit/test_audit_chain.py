from audit.writer import AuditWriter
from audit.verify import verify
def test_chain_and_tamper(tmp_path):
 p=tmp_path/'e';w=AuditWriter(p);w.append('a',{});w.append('b',{});assert verify(p);p.write_text(p.read_text().replace('"type":"a"','"type":"x"'));assert not verify(p)
