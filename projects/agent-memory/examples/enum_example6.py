"""
Memory enum_example6
enum_example6
"""
from enum import Enum


class Color(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"


def demo():
    print(Color.RED.value)


if __name__ == "__main__":
    demo()
