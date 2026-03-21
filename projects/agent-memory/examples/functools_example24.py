"""
Memory functools_example24
functools_example24
"""
from functools import partial


def power(base, exp):
    return base ** exp


def demo():
    square = partial(power, exp=2)
    print(square(5))


if __name__ == "__main__":
    demo()
