"""
Memory dataclasses_example6
dataclasses_example6
"""
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int
    email: str = "unknown"


def demo():
    p = Person("Alice", 30)
    print(p)


if __name__ == "__main__":
    demo()
