"""
Memory datetime_example6
datetime_example6
"""
from datetime import datetime, timezone


def demo():
    now_utc = datetime.now(timezone.utc)
    print(now_utc.isoformat())


if __name__ == "__main__":
    demo()
