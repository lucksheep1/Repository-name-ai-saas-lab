"""
Memory enum_example5
enum_example5
"""
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def demo():
    for c in Color:
        print(c.name, c.value)


if __name__ == "__main__":
    demo()
