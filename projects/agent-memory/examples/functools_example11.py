"""
Memory functools_example11
functools_example11
"""
from functools import reduce


def demo():
    result = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
    print(result)


if __name__ == "__main__":
    demo()
