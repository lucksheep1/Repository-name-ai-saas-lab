"""
Memory dataclasses_example5
dataclasses_example5
"""
from dataclasses import dataclass, asdict


@dataclass
class Point:
    x: int
    y: int


def demo():
    p = Point(1, 2)
    print(asdict(p))


if __name__ == "__main__":
    demo()
