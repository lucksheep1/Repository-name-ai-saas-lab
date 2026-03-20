"""
Memory abc_example18
abc_example18
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass


class Cat(Animal):
    def speak(self):
        return "Meow"


def demo():
    print(Cat().speak())


if __name__ == "__main__":
    demo()
