"""
Memory enum_example19
enum_example19
"""
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


def demo():
    print(Color.RED.name, Color.RED.value)


if __name__ == "__main__":
    demo()
