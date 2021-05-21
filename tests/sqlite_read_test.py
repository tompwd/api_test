import sqlite3


def test_sqlite_read():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM policy")
    rows = cur.fetchall()
    assert len(rows) == 49
