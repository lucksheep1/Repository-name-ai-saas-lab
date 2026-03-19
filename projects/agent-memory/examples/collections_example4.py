"""
Memory collections_example4
collections_example4
"""
from collections import namedtuple


def demo():
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    print(p.x, p.y)


if __name__ == "__main__":
    demo()
