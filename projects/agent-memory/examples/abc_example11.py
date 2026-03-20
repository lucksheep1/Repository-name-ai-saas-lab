"""
Memory abc_example11
abc_example11
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def perimeter(self):
        pass


class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def perimeter(self):
        return self.side * 4


def demo():
    s = Square(5)
    print(s.perimeter())


if __name__ == "__main__":
    demo()
