"""
Memory datetime_example13
datetime_example13
"""
from datetime import timedelta


def demo():
    delta = timedelta(days=5, hours=2)
    print(f"Seconds: {delta.total_seconds()}")


if __name__ == "__main__":
    demo()
