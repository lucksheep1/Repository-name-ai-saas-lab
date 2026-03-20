"""
Memory abc_example14
abc_example14
"""
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, key, value):
        pass
    
    @abstractmethod
    def load(self, key):
        pass


class MemoryStorage(Storage):
    def __init__(self):
        self._data = {}
    
    def save(self, key, value):
        self._data[key] = value
    
    def load(self, key):
        return self._data.get(key)


def demo():
    storage = MemoryStorage()
    storage.save("name", "Alice")
    print(storage.load("name"))


if __name__ == "__main__":
    demo()
