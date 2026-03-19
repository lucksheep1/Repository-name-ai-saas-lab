"""
Memory Sequence
Sequence types
"""
from memory import Memory
from typing import Sequence


def first(items: Sequence) -> any:
    return items[0] if items else None


def demo():
    print(first([1, 2, 3]))


if __name__ == "__main__":
    demo()
