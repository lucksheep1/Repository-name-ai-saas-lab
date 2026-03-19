"""
Memory datetime_example7
datetime_example7
"""
from datetime import datetime, timedelta


def demo():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    print(yesterday.strftime("%Y-%m-%d"))


if __name__ == "__main__":
    demo()
