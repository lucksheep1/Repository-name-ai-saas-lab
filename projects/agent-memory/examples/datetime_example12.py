"""
Memory datetime_example12
datetime_example12
"""
from datetime import datetime, timezone


def demo():
    now_utc = datetime.now(timezone.utc)
    print(now_utc.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    demo()
