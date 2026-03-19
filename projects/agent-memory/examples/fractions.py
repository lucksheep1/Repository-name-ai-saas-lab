"""
Memory fractions
fractions utilities
"""
from fractions import Fraction


def demo():
    f = Fraction(1, 3)
    print(f + Fraction(1, 6))


if __name__ == "__main__":
    demo()
