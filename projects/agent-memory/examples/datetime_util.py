"""
Memory DateTime
DateTime utilities
"""
from memory import Memory
from datetime import datetime, timedelta


def demo():
    now = datetime.now()
    delta = timedelta(days=1)
    print(now + delta)


if __name__ == "__main__":
    demo()
