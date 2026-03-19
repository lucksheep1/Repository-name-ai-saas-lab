"""
Memory datetime_example5
datetime_example5
"""
from datetime import datetime, timedelta


def demo():
    now = datetime.now()
    delta = timedelta(days=30)
    future = now + delta
    print(future.date())


if __name__ == "__main__":
    demo()
