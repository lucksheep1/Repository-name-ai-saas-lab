"""
Memory fractions_example3
fractions_example3
"""
from fractions import Fraction


def demo():
    f1 = Fraction(1, 2)
    f2 = Fraction(3, 4)
    print(f1 + f2)
    print(f1 * f2)


if __name__ == "__main__":
    demo()
