"""
Memory Manager
Manager pattern
"""
from memory import Memory


class Manager:
    def __init__(self):
        self.memories = {}
    
    def create(self, name: str, storage: str = "json"):
        import uuid
        path = f"./{name}_{uuid.uuid4().hex[:8]}.json"
        mem = Memory(storage=storage, path=path)
        self.memories[name] = mem
        return mem
    
    def get(self, name: str):
        return self.memories.get(name)


def demo():
    manager = Manager()
    mem = manager.create("test")
    print(f"Created: {mem}")


if __name__ == "__main__":
    demo()
