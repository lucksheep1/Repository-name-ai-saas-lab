"""
Memory dataclasses_example8
dataclasses_example8
"""
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    
    def __post_init__(self):
        if self.x < 0 or self.y < 0:
            raise ValueError("Coordinates must be positive")


def demo():
    p = Point(1, 2)
    print(p)


if __name__ == "__main__":
    demo()
