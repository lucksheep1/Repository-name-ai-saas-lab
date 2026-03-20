"""
Memory sqlite_example16
sqlite_example16
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x TEXT)")
    conn.execute("INSERT INTO t VALUES (?)", ("test",))
    print(conn.execute("SELECT * FROM t").fetchone())
    conn.close()


if __name__ == "__main__":
    demo()
