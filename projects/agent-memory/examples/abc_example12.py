"""
Memory abc_example12
abc_example12
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def move(self):
        pass


class Dog(Animal):
    def move(self):
        return "running"


def demo():
    print(Dog().move())


if __name__ == "__main__":
    demo()
