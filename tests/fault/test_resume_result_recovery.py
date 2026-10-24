from supervisor.recovery import recover_result
def test_result_recovery(tmp_path):
 d=tmp_path/'c';d.mkdir();assert recover_result(d) is None;(d/'result.json').write_text('{"ok":true}');assert 'true' in recover_result(d)
