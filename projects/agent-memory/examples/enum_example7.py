"""
Memory enum_example7
enum_example7
"""
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    DONE = "done"


def demo():
    print(Status.PENDING.value)


if __name__ == "__main__":
    demo()
