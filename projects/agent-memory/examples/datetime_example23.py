"""
Memory datetime_example23
datetime_example23
"""
from datetime import datetime


def demo():
    dt = datetime.now()
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    demo()
