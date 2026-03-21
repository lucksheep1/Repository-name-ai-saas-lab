"""
Memory sqlite_example22
sqlite_example22
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x)")
    conn.execute("INSERT INTO t VALUES (1), (2), (3)")
    print(conn.execute("SELECT COUNT(*) FROM t").fetchone())
    conn.close()


if __name__ == "__main__":
    demo()
