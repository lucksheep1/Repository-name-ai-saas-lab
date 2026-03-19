"""
Memory functools_example6
functools_example6
"""
from functools import cmp_to_key


def cmp(a, b):
    return (a > b) - (a < b)


def demo():
    sorted([3, 1, 4, 1, 5], key=cmp_to_key(cmp))


if __name__ == "__main__":
    demo()
