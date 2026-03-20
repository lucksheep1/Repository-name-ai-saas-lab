"""
Memory datetime_example11
datetime_example11
"""
from datetime import datetime, timedelta


def demo():
    dt = datetime(2024, 1, 1) + timedelta(days=100)
    print(dt)


if __name__ == "__main__":
    demo()
