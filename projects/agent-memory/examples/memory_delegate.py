"""
Memory Delegate
Delegation pattern
"""
from memory import Memory


class Delegate:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add(self, content: str):
        return self.memory.add(content)


def demo():
    delegate = Delegate(Memory(storage="json", path="test.json"))
    print(delegate.add("Test"))


if __name__ == "__main__":
    demo()
