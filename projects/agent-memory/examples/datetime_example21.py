"""
Memory datetime_example21
datetime_example21
"""
from datetime import datetime, timedelta


def demo():
    dt = datetime.now()
    tomorrow = dt + timedelta(days=1)
    print(tomorrow.date())


if __name__ == "__main__":
    demo()
