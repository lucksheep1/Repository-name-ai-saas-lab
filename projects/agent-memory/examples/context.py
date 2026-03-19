"""
Memory Context
Context manager
"""
from memory import Memory


class MemoryContext:
    def __init__(self, path="ctx.json"):
        self.memory = Memory(storage="json", path=path)
    
    def __enter__(self):
        return self.memory
    
    def __exit__(self, *args):
        pass


def demo():
    with MemoryContext() as mem:
        print(mem.add("Test"))


if __name__ == "__main__":
    demo()
