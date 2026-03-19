"""
Memory abc_example6
abc_example6
"""
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def process(self):
        pass


class Derived(Base):
    def process(self):
        return "processed"


def demo():
    d = Derived()
    print(d.process())


if __name__ == "__main__":
    demo()
