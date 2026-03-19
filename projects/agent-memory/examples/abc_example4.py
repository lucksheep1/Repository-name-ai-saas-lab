"""
Memory abc_example4
abc_example4
"""
from abc import ABC


class Concrete(ABC):
    pass


def demo():
    print(Concrete.__bases__)


if __name__ == "__main__":
    demo()
