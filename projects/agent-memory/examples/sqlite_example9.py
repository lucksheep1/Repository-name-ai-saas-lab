"""
Memory sqlite_example9
sqlite_example9
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)")
    conn.executemany("INSERT INTO test (name, value) VALUES (?, ?)", [("a", 1), ("b", 2)])
    cursor = conn.execute("SELECT * FROM test")
    print(cursor.fetchall())
    conn.close()


if __name__ == "__main__":
    demo()
