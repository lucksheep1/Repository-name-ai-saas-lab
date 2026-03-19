"""
Memory functools_example9
functools_example9
"""
from functools import cached_property


class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @cached_property
    def area(self):
        return 3.14 * self.radius ** 2


def demo():
    c = Circle(5)
    print(c.area)


if __name__ == "__main__":
    demo()
