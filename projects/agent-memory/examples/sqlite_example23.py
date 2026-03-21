"""
Memory sqlite_example23
sqlite_example23
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id, name)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob')")
    for row in conn.execute("SELECT * FROM users"):
        print(row)
    conn.close()


if __name__ == "__main__":
    demo()
