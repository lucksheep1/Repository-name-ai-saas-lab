"""
Memory Generic
Generic types
"""
from memory import Memory
from typing import TypeVar, Generic


T = TypeVar("T")


class Container(Generic[T]):
    def __init__(self, value: T):
        self.value = value


def demo():
    c = Container("test")
    print(c.value)


if __name__ == "__main__":
    demo()
