"""
Memory sqlite_example24
sqlite_example24
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO t (name) VALUES (?)", ("Alice",))
    print(conn.lastrowid)
    conn.close()


if __name__ == "__main__":
    demo()
