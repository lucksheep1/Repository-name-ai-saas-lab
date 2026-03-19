"""
Memory abc_example5
abc_example5
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14 * self.radius ** 2


def demo():
    c = Circle(5)
    print(c.area())


if __name__ == "__main__":
    demo()
