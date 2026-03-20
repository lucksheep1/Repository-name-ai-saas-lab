"""
Memory enum_example17
enum_example17
"""
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def demo():
    print(list(Color))


if __name__ == "__main__":
    demo()
