"""
Memory abc_example19
abc_example19
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, r):
        self.r = r
    
    def area(self):
        return 3.14 * self.r ** 2


def demo():
    print(Circle(2).area())


if __name__ == "__main__":
    demo()
