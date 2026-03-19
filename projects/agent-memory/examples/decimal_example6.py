"""
Memory decimal_example6
decimal_example6
"""
from decimal import Decimal, getcontext


def demo():
    getcontext().prec = 6
    print(Decimal("1") / Decimal("7"))


if __name__ == "__main__":
    demo()
