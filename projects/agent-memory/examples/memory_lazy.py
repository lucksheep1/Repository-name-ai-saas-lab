"""
Memory Lazy Load
Lazy loading pattern
"""
from memory import Memory


class LazyMemory:
    def __init__(self):
        self._memory = None
        self._loaded = False
    
    @property
    def memory(self):
        if not self._loaded:
            self._memory = Memory(storage="json", path="./lazy.json")
            self._loaded = True
        return self._memory
    
    def add(self, content: str, **kwargs):
        return self.memory.add(content, **kwargs)
    
    def get_all(self):
        return self.memory.get_all()


def demo():
    lazy = LazyMemory()
    
    # Not loaded yet
    print(f"Added: {lazy.add('Test')}")


if __name__ == "__main__":
    demo()
