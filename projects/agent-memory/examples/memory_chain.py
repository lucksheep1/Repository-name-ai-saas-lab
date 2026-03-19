"""
Memory Chain
Chain of responsibility
"""
from memory import Memory


class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler
    
    def handle(self, request: str):
        if self.next:
            return self.next.handle(request)


class AddHandler(Handler):
    def __init__(self, memory: Memory, next_handler=None):
        super().__init__(next_handler)
        self.memory = memory
    
    def handle(self, request: str):
        if request.startswith("add:"):
            content = request[4:]
            return self.memory.add(content)
        
        return super().handle(request)


def demo():
    memory = Memory(storage="json", path="./chain_demo.json")
    handler = AddHandler(memory)
    
    handler.handle("add:Test")
    print(f"Count: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
