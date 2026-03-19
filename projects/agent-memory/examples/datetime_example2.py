"""
Memory datetime_example2
datetime_example2
"""
from datetime import datetime, timedelta


def demo():
    now = datetime.now()
    future = now + timedelta(days=7)
    print(future.strftime("%Y-%m-%d"))


if __name__ == "__main__":
    demo()
