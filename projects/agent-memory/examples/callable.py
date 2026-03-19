"""
Memory Callable
Callable types
"""
from memory import Memory
from typing import Callable


def apply(func: Callable[[int], int], x: int) -> int:
    return func(x)


def double(x: int) -> int:
    return x * 2


def demo():
    print(apply(double, 5))


if __name__ == "__main__":
    demo()
