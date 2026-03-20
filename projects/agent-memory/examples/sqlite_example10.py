"""
Memory sqlite_example10
sqlite_example10
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO test (value) VALUES (?)", ("test",))
    print(conn.total_changes)
    conn.close()


if __name__ == "__main__":
    demo()
