"""
Memory sqlite_example5
sqlite_example5
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)")
    conn.executemany("INSERT INTO test (name, value) VALUES (?, ?)", [("a", 1), ("b", 2), ("c", 3)])
    for row in conn.execute("SELECT * FROM test WHERE value > 1"):
        print(row)


if __name__ == "__main__":
    demo()
