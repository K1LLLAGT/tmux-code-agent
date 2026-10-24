from fsguard.atomic import atomic_write
def test_repeated_atomic_write_leaves_complete_value(tmp_path):
 p=tmp_path/'x';atomic_write(p,b'A'*1000);atomic_write(p,b'B'*1000);assert p.read_bytes()==b'B'*1000
