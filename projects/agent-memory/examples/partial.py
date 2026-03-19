"""
Memory Partial
Partial application
"""
from memory import Memory
from functools import partial


def add(a, b, c):
    return a + b + c


def demo():
    add_1 = partial(add, 1)
    add_1_2 = partial(add_1, 2)
    print(add_1_2(3))


if __name__ == "__main__":
    demo()
