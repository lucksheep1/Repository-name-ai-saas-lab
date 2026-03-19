"""
Memory decimal_example2
decimal_example2
"""
from decimal import Decimal, getcontext


def demo():
    getcontext().prec = 10
    print(Decimal("1") / Decimal("7"))


if __name__ == "__main__":
    demo()
