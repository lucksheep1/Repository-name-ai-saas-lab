"""
Memory sqlite_example14
sqlite_example14
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    conn.executemany("INSERT INTO test (value) VALUES (?)", [("a",), ("b",), ("c",)])
    cursor = conn.execute("SELECT * FROM test")
    print(list(cursor))
    conn.close()


if __name__ == "__main__":
    demo()
