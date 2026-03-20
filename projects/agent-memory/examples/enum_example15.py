"""
Memory enum_example15
enum_example15
"""
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def demo():
    for d in Direction:
        print(d.name, d.value)


if __name__ == "__main__":
    demo()
