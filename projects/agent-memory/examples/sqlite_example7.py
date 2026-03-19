"""
Memory sqlite_example7
sqlite_example7
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob')")
    print(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])


if __name__ == "__main__":
    demo()
