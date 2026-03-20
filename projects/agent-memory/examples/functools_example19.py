"""
Memory functools_example19
functools_example19
"""
from functools import partial


def add(a, b, c):
    return a + b + c


def demo():
    add_5 = partial(add, 5)
    print(add_5(1, 2))


if __name__ == "__main__":
    demo()
