"""
Memory sqlite_example19
sqlite_example19
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x)")
    conn.execute("INSERT INTO t VALUES (1)")
    print(conn.execute("SELECT * FROM t").fetchone())
    conn.close()


if __name__ == "__main__":
    demo()
