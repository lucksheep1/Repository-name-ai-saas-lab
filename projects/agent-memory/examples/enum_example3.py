"""
Memory enum_example3
enum_example3
"""
from enum import Flag, auto


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


def demo():
    print(Perm.READ | Perm.WRITE)


if __name__ == "__main__":
    demo()
