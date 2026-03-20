"""
Memory sqlite_example15
sqlite_example15
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO t (name) VALUES ('Alice')")
    conn.execute("INSERT INTO t (name) VALUES ('Bob')")
    print(conn.total_changes)
    conn.close()


if __name__ == "__main__":
    demo()
