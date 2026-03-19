"""
Memory typing_example
typing_example
"""
from typing import List


def process(items: List[int]) -> int:
    return sum(items)


def demo():
    print(process([1, 2, 3]))


if __name__ == "__main__":
    demo()
