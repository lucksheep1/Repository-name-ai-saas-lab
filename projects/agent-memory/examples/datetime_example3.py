"""
Memory datetime_example3
datetime_example3
"""
from datetime import datetime, timezone


def demo():
    now_utc = datetime.now(timezone.utc)
    print(now_utc.isoformat())


if __name__ == "__main__":
    demo()
