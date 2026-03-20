"""
Memory typing_example12
typing_example12
"""
from typing import Tuple


def process() -> Tuple[int, str]:
    return 42, "answer"


def demo():
    print(process())


if __name__ == "__main__":
    demo()
