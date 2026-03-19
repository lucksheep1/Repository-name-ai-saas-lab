"""
Memory enum_example9
enum_example9
"""
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def demo():
    print(Color.RED.name)


if __name__ == "__main__":
    demo()
