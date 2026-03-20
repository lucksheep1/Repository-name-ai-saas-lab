"""
Memory functools_example23
functools_example23
"""
from functools import reduce


def mul(a, b):
    return a * b


def demo():
    print(reduce(mul, [1, 2, 3, 4]))


if __name__ == "__main__":
    demo()
