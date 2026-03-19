"""
Memory datetime
datetime utilities
"""
from datetime import datetime, timedelta


def demo():
    now = datetime.now()
    print(now + timedelta(days=7))


if __name__ == "__main__":
    demo()
