"""
Memory typing_example9
typing_example9
"""
from typing import Any, Union


def process(value: Any) -> Union[str, int]:
    return str(value)


def demo():
    print(process(42))
    print(process("hello"))


if __name__ == "__main__":
    demo()
