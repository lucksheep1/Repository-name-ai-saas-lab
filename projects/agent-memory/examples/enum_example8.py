"""
Memory enum_example8
enum_example8
"""
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


def demo():
    print(Status.PENDING.value)


if __name__ == "__main__":
    demo()
