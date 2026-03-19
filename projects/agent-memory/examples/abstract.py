"""
Memory Abstract
Abstract classes
"""
from memory import Memory
from abc import ABC, abstractmethod


class AbstractMemory(ABC):
    @abstractmethod
    def add(self, content: str):
        pass


class ConcreteMemory(AbstractMemory):
    def __init__(self):
        self.memory = Memory(storage="json", path="test.json")
    
    def add(self, content: str):
        return self.memory.add(content)


def demo():
    mem = ConcreteMemory()
    print(mem.add("Test"))


if __name__ == "__main__":
    demo()
