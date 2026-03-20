"""
Memory dataclasses_example19
dataclasses_example19
"""
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int


def demo():
    p = Person("Alice", 30)
    print(p)


if __name__ == "__main__":
    demo()
