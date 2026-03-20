"""
Memory datetime_example11
datetime_example11
"""
from datetime import datetime, timedelta


def demo():
    dt1 = datetime(2024, 1, 1)
    dt2 = dt1 + timedelta(days=30)
    print(dt2)


if __name__ == "__main__":
    demo()
