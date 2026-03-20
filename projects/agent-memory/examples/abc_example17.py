"""
Memory abc_example17
abc_example17
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2


def demo():
    print(Circle(2).area())


if __name__ == "__main__":
    demo()
