"""
Memory Trait
Traits (Python 3.11+)
"""
from memory import Memory


class AddTrait:
    def add(self, content: str):
        return self.memory.add(content)


class SearchTrait:
    def search(self, query: str):
        return self.memory.search(query)


class ExtendedMemory(AddTrait, SearchTrait):
    def __init__(self):
        self.memory = Memory(storage="json", path="test.json")


def demo():
    mem = ExtendedMemory()
    print(mem.add("Test"))


if __name__ == "__main__":
    demo()
