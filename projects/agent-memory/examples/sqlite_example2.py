"""
Memory sqlite_example2
sqlite_example2
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INT, name TEXT)")
    conn.execute("INSERT INTO test VALUES (1, 'alice')")
    print(conn.execute("SELECT * FROM test").fetchone())


if __name__ == "__main__":
    demo()
