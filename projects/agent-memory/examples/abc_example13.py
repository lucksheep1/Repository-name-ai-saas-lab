"""
Memory abc_example13
abc_example13
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


def demo():
    rect = Rectangle(5, 3)
    print(f"Area: {rect.area()}, Perimeter: {rect.perimeter()}")


if __name__ == "__main__":
    demo()
