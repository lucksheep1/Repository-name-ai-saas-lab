"""
Memory Visitor
Visitor pattern for memory
"""
from memory import Memory


class Visitor:
    def visit(self, mem: dict):
        raise NotImplementedError


class PrintVisitor(Visitor):
    def visit(self, mem: dict):
        print(f"- {mem.get('content')}")


class CountVisitor(Visitor):
    def __init__(self):
        self.count = 0
    
    def visit(self, mem: dict):
        self.count += 1


class MemoryVisitor:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def accept(self, visitor: Visitor):
        for mem in self.memory.get_all():
            visitor.visit(mem)


def demo():
    memory = Memory(storage="json", path="./visitor_demo.json")
    memory.add("A")
    memory.add("B")
    
    visitor = MemoryVisitor(memory)
    counter = CountVisitor()
    
    visitor.accept(counter)
    print(f"Count: {counter.count}")


if __name__ == "__main__":
    demo()
