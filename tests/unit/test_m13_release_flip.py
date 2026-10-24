from core.releases import flip,rollback
def test_flip_rollback(tmp_path):
 (tmp_path/'releases/a').mkdir(parents=True);(tmp_path/'releases/b').mkdir();flip(tmp_path,'a');assert (tmp_path/'current').resolve().name=='a';flip(tmp_path,'b');assert (tmp_path/'current').resolve().name=='b';rollback(tmp_path,'a');assert (tmp_path/'current').resolve().name=='a'
