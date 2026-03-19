"""
Memory functools_example10
functools_example10
"""
from functools import partial


def power(base, exponent):
    return base ** exponent


def demo():
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    print(square(5))
    print(cube(5))


if __name__ == "__main__":
    demo()
