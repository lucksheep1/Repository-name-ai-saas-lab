"""
Memory functools_example20
functools_example20
"""
from functools import cmp_to_key


def cmp(a, b):
    return b - a


def demo():
    sorted([3, 1, 4, 1, 5], key=cmp_to_key(cmp))
    print("Sorted")


if __name__ == "__main__":
    demo()
