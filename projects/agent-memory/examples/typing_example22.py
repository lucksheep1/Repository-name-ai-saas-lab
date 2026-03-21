"""
Memory typing_example22
typing_example22
"""
from typing import List, Dict


def process(items: List[int]) -> Dict[str, int]:
    return {"sum": sum(items), "count": len(items)}


def demo():
    print(process([1, 2, 3]))


if __name__ == "__main__":
    demo()
