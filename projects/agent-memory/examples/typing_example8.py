"""
Memory typing_example8
typing_example8
"""
from typing import Set


def process(items: Set[int]) -> int:
    return sum(items)


def demo():
    print(process({1, 2, 3, 4}))


if __name__ == "__main__":
    demo()
