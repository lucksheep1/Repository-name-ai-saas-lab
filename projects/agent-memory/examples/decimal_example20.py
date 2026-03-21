"""
Memory decimal_example20
decimal_example20
"""
from decimal import Decimal, getcontext


def demo():
    getcontext().prec = 5
    print(Decimal("1") / Decimal("7"))


if __name__ == "__main__":
    demo()
