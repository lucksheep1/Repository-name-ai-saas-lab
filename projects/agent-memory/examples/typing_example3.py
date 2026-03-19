"""
Memory typing_example3
typing_example3
"""
from typing import Callable


def apply(func: Callable[[int], int], x: int) -> int:
    return func(x)


def demo():
    print(apply(lambda x: x * 2, 5))


if __name__ == "__main__":
    demo()
