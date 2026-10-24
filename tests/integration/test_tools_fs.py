from tools.fs_tools import write_file,read_file
def test_write_stale_read(tmp_path):
 w=tmp_path/'w';w.mkdir();r=write_file(w,'a.txt','one');assert r['ok'];h=r['data']['sha256'];assert read_file(w,'a.txt')['data']['content']=='one';assert write_file(w,'a.txt','two','bad')['error']['code']=='ERR_STALE_FILE';assert write_file(w,'a.txt','two',h)['ok']
