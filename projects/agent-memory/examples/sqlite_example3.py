"""
Memory sqlite_example3
sqlite_example3
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT, name TEXT, email TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", [(1, "Alice", "a@b.c"), (2, "Bob", "b@c.d")])
    for row in conn.execute("SELECT * FROM users"):
        print(row)


if __name__ == "__main__":
    demo()
