"""
Memory sqlite_example17
sqlite_example17
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (x)")
    conn.execute("INSERT INTO t VALUES (1)")
    print(conn.in_transaction)
    conn.close()


if __name__ == "__main__":
    demo()
