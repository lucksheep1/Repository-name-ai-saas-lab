"""
Memory abc_example9
abc_example9
"""
from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "Woof"


def demo():
    print(Dog().speak())


if __name__ == "__main__":
    demo()
