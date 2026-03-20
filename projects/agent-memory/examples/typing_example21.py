"""
Memory typing_example21
typing_example21
"""
from typing import Tuple


def process() -> Tuple[int, str]:
    return (1, "hello")


def demo():
    print(process())


if __name__ == "__main__":
    demo()
