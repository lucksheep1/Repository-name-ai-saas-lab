"""
Memory enum_example12
enum_example12
"""
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def demo():
    print([d.name for d in Direction])


if __name__ == "__main__":
    demo()
