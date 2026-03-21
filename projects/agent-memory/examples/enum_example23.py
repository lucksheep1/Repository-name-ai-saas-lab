"""
Memory enum_example23
enum_example23
"""
from enum import Flag, auto


class Permissions(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


def demo():
    print(Permissions.READ | Permissions.WRITE)


if __name__ == "__main__":
    demo()
