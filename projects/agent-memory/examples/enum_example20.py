"""
Memory enum_example20
enum_example20
"""
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    DONE = "done"


def demo():
    print(Status.PENDING.value)


if __name__ == "__main__":
    demo()
