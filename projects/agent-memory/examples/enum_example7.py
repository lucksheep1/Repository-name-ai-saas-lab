"""
Memory enum_example7
enum_example7
"""
from enum import Enum, auto


class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


def demo():
    print(list(Priority))


if __name__ == "__main__":
    demo()
