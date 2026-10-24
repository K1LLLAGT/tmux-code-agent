from store.db import open_db
def test_db(tmp_path):
 c=open_db(tmp_path/'s.db');assert c.execute('PRAGMA user_version').fetchone()[0]==1;assert c.execute("select name from sqlite_master where name='tasks'").fetchone();c.close()
