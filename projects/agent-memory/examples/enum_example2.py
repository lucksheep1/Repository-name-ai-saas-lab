"""
Memory enum_example2
enum_example2
"""
from enum import IntEnum


class Status(IntEnum):
    PENDING = 1
    DONE = 2
    ERROR = 3


def demo():
    print(Status.PENDING == 1)


if __name__ == "__main__":
    demo()
