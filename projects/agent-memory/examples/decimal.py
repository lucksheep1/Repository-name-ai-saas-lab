"""
Memory decimal
decimal utilities
"""
from decimal import Decimal


def demo():
    d = Decimal("0.1") + Decimal("0.2")
    print(d)


if __name__ == "__main__":
    demo()
