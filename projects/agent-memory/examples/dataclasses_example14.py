"""
Memory dataclasses_example14
dataclasses_example14
"""
from dataclasses import dataclass, asdict


@dataclass
class Person:
    name: str
    age: int


def demo():
    p = Person("Alice", 30)
    print(asdict(p))


if __name__ == "__main__":
    demo()
