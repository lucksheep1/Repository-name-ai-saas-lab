"""
Memory sqlite_example21
sqlite_example21
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x, y)")
    conn.execute("INSERT INTO t VALUES (1, 2)")
    print(conn.execute("SELECT * FROM t").fetchall())
    conn.close()


if __name__ == "__main__":
    demo()
