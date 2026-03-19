"""
Memory functools_example2
functools_example2
"""
from functools import partial


def add(a, b):
    return a + b


def demo():
    add5 = partial(add, 5)
    print(add5(10))


if __name__ == "__main__":
    demo()
