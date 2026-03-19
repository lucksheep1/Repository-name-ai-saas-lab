"""
Memory typing
typing utilities
"""
from typing import List, Dict, Optional


def process(items: List[int]) -> Dict[str, int]:
    return {"sum": sum(items)}


def demo():
    result = process([1, 2, 3])
    print(result)


if __name__ == "__main__":
    demo()
