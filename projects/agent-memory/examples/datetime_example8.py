"""
Memory datetime_example8
datetime_example8
"""
from datetime import datetime, timezone


def demo():
    dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    print(dt.timestamp())


if __name__ == "__main__":
    demo()
