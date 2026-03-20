"""
Memory dataclasses_example13
dataclasses_example13
"""
from dataclasses import fields


@dataclass
class Point:
    x: int
    y: int


def demo():
    print(len(fields(Point)))


if __name__ == "__main__":
    demo()
