"""
Memory enum_example14
enum_example14
"""
from enum import IntEnum


class Color(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3


def demo():
    print(Color.RED + Color.GREEN)
    print(Color(2))


if __name__ == "__main__":
    demo()
