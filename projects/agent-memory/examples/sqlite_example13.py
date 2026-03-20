"""
Memory sqlite_example13
sqlite_example13
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Apple", 1.50))
    conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", ("Banana", 0.75))
    for row in conn.execute("SELECT * FROM items WHERE price < 1.0"):
        print(row)
    conn.close()


if __name__ == "__main__":
    demo()
