"""
Memory Any
Any type
"""
from memory import Memory
from typing import Any


def process(value: Any) -> str:
    return str(value)


def demo():
    print(process(123))
    print(process("test"))


if __name__ == "__main__":
    demo()
