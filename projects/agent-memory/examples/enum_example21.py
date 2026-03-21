"""
Memory enum_example21
enum_example21
"""
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def demo():
    print([d.name for d in Direction])


if __name__ == "__main__":
    demo()
