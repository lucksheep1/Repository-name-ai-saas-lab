"""
Memory dataclasses_example
dataclasses_example
"""
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def demo():
    print(Point(1, 2))


if __name__ == "__main__":
    demo()
