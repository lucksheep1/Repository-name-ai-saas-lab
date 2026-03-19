"""
Memory dataclasses_example11
dataclasses_example11
"""
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
    
    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5


def demo():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(p1.distance_to(p2))


if __name__ == "__main__":
    demo()
