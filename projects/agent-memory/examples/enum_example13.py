"""
Memory enum_example13
enum_example13
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
