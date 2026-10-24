from core.releases import flip
def test_live_file_unmodified_by_flip(tmp_path):
 (tmp_path/'releases/a').mkdir(parents=True);(tmp_path/'releases/b').mkdir();live=tmp_path/'live';live.write_text('session-old-code');flip(tmp_path,'a');flip(tmp_path,'b');assert live.read_text()=='session-old-code'
