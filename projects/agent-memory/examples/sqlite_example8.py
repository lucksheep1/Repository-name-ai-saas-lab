"""
Memory sqlite_example8
sqlite_example8
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES ('Alice')")
    conn.execute("INSERT INTO test (name) VALUES ('Bob')")
    cursor = conn.execute("SELECT * FROM test WHERE name = ?", ("Alice",))
    print(cursor.fetchone())
    conn.close()


if __name__ == "__main__":
    demo()
