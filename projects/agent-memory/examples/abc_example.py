"""
Memory abc_example
abc_example
"""
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def process(self):
        pass


def demo():
    print("abc ready")


if __name__ == "__main__":
    demo()
