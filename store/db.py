import sqlite3
from pathlib import Path
def open_db(path:Path):
 con=sqlite3.connect(path);con.execute('PRAGMA journal_mode=WAL');con.execute('PRAGMA synchronous=NORMAL');sql=(Path(__file__).parent/'migrations/0001_init.sql').read_text();con.executescript(sql);con.execute('PRAGMA user_version=1');con.commit();return con
