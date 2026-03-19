"""
Memory typing_example11
typing_example11
"""
from typing import List, Optional


def find_item(items: List[int], target: int) -> Optional[int]:
    for i, item in enumerate(items):
        if item == target:
            return i
    return None


def demo():
    print(find_item([1, 2, 3], 2))


if __name__ == "__main__":
    demo()
