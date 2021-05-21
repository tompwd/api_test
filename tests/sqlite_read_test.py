import sqlite3


def test_sqlite_read_policy():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM policy")
    rows = cur.fetchall()
    assert len(rows) == 49


def test_sqlite_read_finance():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM finance")
    rows = cur.fetchall()
    assert len(rows) == 49


def test_sqlite_read_calendar():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM calendar")
    rows = cur.fetchall()
    assert len(rows) == 389


def test_sqlite_read_policy_lifecycle():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM policy_lifecycle")
    rows = cur.fetchall()
    assert len(rows) == 127
