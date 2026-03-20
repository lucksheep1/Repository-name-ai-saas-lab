"""
Memory typing_example14
typing_example14
"""
from typing import Union


def process(value: Union[int, str]) -> str:
    return str(value)


def demo():
    print(process(42))
    print(process("hello"))


if __name__ == "__main__":
    demo()
