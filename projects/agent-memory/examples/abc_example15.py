"""
Memory abc_example15
abc_example15
"""
from abc import ABC, abstractmethod


class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass


class Bird(Flyable):
    def fly(self):
        return "Flying high"


def demo():
    print(Bird().fly())


if __name__ == "__main__":
    demo()
