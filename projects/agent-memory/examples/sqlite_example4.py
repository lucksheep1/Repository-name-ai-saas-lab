"""
Memory sqlite_example4
sqlite_example4
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO test (value) VALUES (?)", ("test",))
    conn.commit()
    print(conn.total_changes)


if __name__ == "__main__":
    demo()
