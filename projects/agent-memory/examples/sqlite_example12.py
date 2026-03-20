"""
Memory sqlite_example12
sqlite_example12
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    conn.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    for row in conn.execute("SELECT * FROM users"):
        print(row)
    conn.close()


if __name__ == "__main__":
    demo()
