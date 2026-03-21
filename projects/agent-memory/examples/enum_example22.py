"""
Memory enum_example22
enum_example22
"""
from enum import Enum, IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def demo():
    print(Priority.HIGH > Priority.LOW)


if __name__ == "__main__":
    demo()
