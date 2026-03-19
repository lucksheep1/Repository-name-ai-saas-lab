"""
Memory Iterable
Iterable types
"""
from memory import Memory
from typing import Iterable


def iterate(items: Iterable[str]) -> list:
    return list(items)


def demo():
    print(iterate(["a", "b", "c"]))


if __name__ == "__main__":
    demo()
