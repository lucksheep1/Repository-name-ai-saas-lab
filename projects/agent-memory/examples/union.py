"""
Memory Union
Union types
"""
from memory import Memory
from typing import Union


def process(value: Union[str, int]) -> str:
    return str(value)


def demo():
    print(process("test"))
    print(process(123))


if __name__ == "__main__":
    demo()
