"""
Memory typing_example8
typing_example8
"""
from typing import Dict


def process(data: Dict[str, int]) -> int:
    return sum(data.values())


def demo():
    print(process({"a": 1, "b": 2, "c": 3}))


if __name__ == "__main__":
    demo()
