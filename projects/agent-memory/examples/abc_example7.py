"""
Memory abc_example7
abc_example7
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


def demo():
    animals = [Dog(), Cat()]
    for animal in animals:
        print(animal.speak())


if __name__ == "__main__":
    demo()
