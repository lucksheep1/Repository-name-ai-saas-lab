"""
Memory typing_example18
typing_example18
"""
from typing import Tuple


def process() -> Tuple[int, str, bool]:
    return (1, "hello", True)


def demo():
    result = process()
    print(result)


if __name__ == "__main__":
    demo()
