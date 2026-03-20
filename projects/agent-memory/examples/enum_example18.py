"""
Memory enum_example18
enum_example18
"""
from enum import Enum


class Status(Enum):
    SUCCESS = 1
    ERROR = 2


def demo():
    print(Status.SUCCESS.name)


if __name__ == "__main__":
    demo()
