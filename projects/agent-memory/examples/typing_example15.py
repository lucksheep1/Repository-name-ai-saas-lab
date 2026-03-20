"""
Memory typing_example15
typing_example15
"""
from typing import List


def process(items: List[int]) -> int:
    return sum(items)


def demo():
    print(process([1, 2, 3, 4, 5]))


if __name__ == "__main__":
    demo()
