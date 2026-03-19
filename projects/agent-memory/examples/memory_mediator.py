"""
Memory Mediator
Mediator pattern for memory
"""
from memory import Memory


class Mediator:
    def __init__(self):
        self.components = []
    
    def add(self, component):
        self.components.append(component)
    
    def notify(self, sender, event: str):
        for comp in self.components:
            if comp != sender:
                comp.handle(event)


class Component:
    def __init__(self, memory: Memory, mediator: Mediator):
        self.memory = memory
        self.mediator = mediator
    
    def handle(self, event: str):
        pass


class Adder(Component):
    def add(self, content: str):
        self.memory.add(content)
        self.mediator.notify(self, "added")


class Searcher(Component):
    def handle(self, event: str):
        print(f"Searcher handled: {event}")


def demo():
    med = Mediator()
    
    adder = Adder(Memory(storage="json", path="./mediator1.json"), med)
    searcher = Searcher(Memory(storage="json", path="./mediator2.json"), med)
    
    med.add(adder)
    med.add(searcher)
    
    adder.add("Test")


if __name__ == "__main__":
    demo()
