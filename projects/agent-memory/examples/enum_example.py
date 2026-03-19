"""
Memory enum_example
enum_example
"""
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()


def demo():
    print(Color.RED.name)


if __name__ == "__main__":
    demo()
