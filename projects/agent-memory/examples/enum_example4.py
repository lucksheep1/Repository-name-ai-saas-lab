"""
Memory enum_example4
enum_example4
"""
from enum import Enum, member


class Status(Enum):
    PENDING = 1
    DONE = 2


def demo():
    print(list(Status))


if __name__ == "__main__":
    demo()
