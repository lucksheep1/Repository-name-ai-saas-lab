"""
Memory Iterator
Iterator pattern for memory
"""
from memory import Memory


class MemoryIterator:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.index = 0
        self.items = memory.get_all()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        
        item = self.items[self.index]
        self.index += 1
        return item


def demo():
    memory = Memory(storage="json", path="./iterator_demo.json")
    
    memory.add("A")
    memory.add("B")
    memory.add("C")
    
    for mem in MemoryIterator(memory):
        print(mem.get("content"))


if __name__ == "__main__":
    demo()
