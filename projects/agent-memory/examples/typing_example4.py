"""
Memory typing_example4
typing_example4
"""
from typing import Any


def demo():
    x: Any = "string"
    x = 123
    print(x)


if __name__ == "__main__":
    demo()
