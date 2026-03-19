"""
Memory sqlite_example7
sqlite_example7
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES (?)", ("Alice",))
    conn.execute("INSERT INTO test (name) VALUES (?)", ("Bob",))
    cursor = conn.execute("SELECT * FROM test")
    for row in cursor:
        print(row)
    conn.close()


if __name__ == "__main__":
    demo()
