"""
Memory datetime_example4
datetime_example4
"""
from datetime import datetime


def demo():
    dt = datetime(2024, 1, 15, 10, 30, 0)
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    demo()
