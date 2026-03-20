"""
Memory sqlite_example12
sqlite_example12
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO test (value) VALUES (?)", ("test",))
    result = conn.execute("SELECT * FROM test").fetchone()
    print(result)
    conn.close()


if __name__ == "__main__":
    demo()
