"""
Memory functools_example3
functools_example3
"""
from functools import reduce


def add(a, b):
    return a + b


def demo():
    print(reduce(add, [1, 2, 3, 4, 5]))


if __name__ == "__main__":
    demo()
