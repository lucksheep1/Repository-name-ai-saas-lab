"""
Memory enum_example10
enum_example10
"""
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def demo():
    print(Priority.LOW + 1)


if __name__ == "__main__":
    demo()
