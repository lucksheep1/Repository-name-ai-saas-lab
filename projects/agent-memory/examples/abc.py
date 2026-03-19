"""
Memory abc
abc utilities
"""
from memory import Memory
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def process(self):
        pass


class Derived(Base):
    def process(self):
        return "done"


def demo():
    d = Derived()
    print(d.process())


if __name__ == "__main__":
    demo()
