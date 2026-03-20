"""
Memory sqlite_example18
sqlite_example18
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("SELECT 1")
    print(conn.total_changes)
    conn.close()


if __name__ == "__main__":
    demo()
