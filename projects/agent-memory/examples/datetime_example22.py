"""
Memory datetime_example22
datetime_example22
"""
from datetime import datetime


def demo():
    dt1 = datetime(2024, 1, 1)
    dt2 = datetime(2024, 12, 31)
    print((dt2 - dt1).days)


if __name__ == "__main__":
    demo()
