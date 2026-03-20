"""
Memory dataclasses_example20
dataclasses_example20
"""
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int = 0


def demo():
    p = Person("Alice", 30)
    print(p.name, p.age)


if __name__ == "__main__":
    demo()
