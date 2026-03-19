"""
Memory abc_example3
abc_example3
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    def speak(self) -> str:
        return "Woof"


def demo():
    dog = Dog()
    print(dog.speak())


if __name__ == "__main__":
    demo()
