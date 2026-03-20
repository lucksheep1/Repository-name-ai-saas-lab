"""
Memory decimal_example10
decimal_example10
"""
from decimal import Decimal, getcontext


def demo():
    getcontext().prec = 50
    print(Decimal(1) / Decimal(7))


if __name__ == "__main__":
    demo()
