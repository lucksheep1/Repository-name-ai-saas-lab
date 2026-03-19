"""
Memory abc_example6
abc_example6
"""
from abc import ABC


class MyClass(ABC):
    pass


def demo():
    print(MyClass.__bases__)


if __name__ == "__main__":
    demo()
