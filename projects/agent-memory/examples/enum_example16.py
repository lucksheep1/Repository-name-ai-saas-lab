"""
Memory enum_example16
enum_example16
"""
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"


def demo():
    print(Status.PENDING.value)


if __name__ == "__main__":
    demo()
