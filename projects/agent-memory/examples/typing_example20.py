"""
Memory typing_example20
typing_example20
"""
from typing import Dict


def process(data: Dict[str, int]) -> int:
    return sum(data.values())


def demo():
    print(process({"a": 1, "b": 2}))


if __name__ == "__main__":
    demo()
