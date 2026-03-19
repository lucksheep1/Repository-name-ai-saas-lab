"""
Memory Service
Service layer
"""
from memory import Memory


class Service:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add_memory(self, content: str, tags: list = None):
        return self.memory.add(content, tags=tags or [])
    
    def get_memories(self):
        return self.memory.get_all()


def demo():
    service = Service(Memory(storage="json", path="test.json"))
    print(service.add_memory("Test"))


if __name__ == "__main__":
    demo()
