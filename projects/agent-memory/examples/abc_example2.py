"""
Memory abc_example2
abc_example2
"""
from abc import ABC


class MyABC(ABC):
    pass


def demo():
    print(MyABC.__bases__)


if __name__ == "__main__":
    demo()
