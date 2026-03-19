"""
Memory typing_example5
typing_example5
"""
from typing import Generic, TypeVar


T = TypeVar("T")


class Container(Generic[T]):
    def __init__(self, value: T):
        self.value = value


def demo():
    c: Container[int] = Container(42)
    print(c.value)


if __name__ == "__main__":
    demo()
