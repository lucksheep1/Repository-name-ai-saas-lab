"""
Memory sqlite_example
sqlite_example
"""
import sqlite3


def demo():
    conn = sqlite3.connect(":memory:")
    print(conn)


if __name__ == "__main__":
    demo()
