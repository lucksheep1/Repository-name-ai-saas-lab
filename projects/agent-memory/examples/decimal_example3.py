"""
Memory decimal_example3
decimal_example3
"""
from decimal import Decimal, ROUND_HALF_UP


def demo():
    d = Decimal("2.5")
    rounded = d.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    print(rounded)


if __name__ == "__main__":
    demo()
