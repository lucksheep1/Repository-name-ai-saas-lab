"""
Memory functools_example18
functools_example18
"""
from functools import reduce


def add(x, y):
    return x + y


def demo():
    print(reduce(add, [1, 2, 3, 4, 5]))


if __name__ == "__main__":
    demo()
