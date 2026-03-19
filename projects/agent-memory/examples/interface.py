"""
Memory Interface
Interfaces
"""
from memory import Memory


class IMemory:
    def add(self, content: str):
        raise NotImplementedError
    
    def search(self, query: str):
        raise NotImplementedError


class Implementation(IMemory):
    def __init__(self):
        self.memory = Memory(storage="json", path="test.json")
    
    def add(self, content: str):
        return self.memory.add(content)
    
    def search(self, query: str):
        return self.memory.search(query)


def demo():
    impl = Implementation()
    print(impl.add("Test"))


if __name__ == "__main__":
    demo()
