"""
Memory Overload
Function overloading
"""
from memory import Memory
from typing import overload


@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...


def process(x):
    return x


def demo():
    print(process(1))
    print(process("test"))


if __name__ == "__main__":
    demo()
