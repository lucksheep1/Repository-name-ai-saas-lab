"""
Memory typing_example6
typing_example6
"""
from typing import Tuple


def process() -> Tuple[int, str]:
    return (1, "one")


def demo():
    print(process())


if __name__ == "__main__":
    demo()
