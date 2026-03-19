"""
Memory sqlite_example6
sqlite_example6
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES (?)", ("test",))
    cursor = conn.execute("SELECT * FROM test")
    print(cursor.fetchone())


if __name__ == "__main__":
    demo()
