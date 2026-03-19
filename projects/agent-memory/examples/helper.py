"""
Memory Helper
Helper functions
"""
from memory import Memory


def create_memory(storage="json", path="memory.json"):
    return Memory(storage=storage, path=path)


def quick_add(memory, content, tags=None):
    return memory.add(content, tags=tags or [])


def demo():
    mem = create_memory()
    print(quick_add(mem, "Test"))


if __name__ == "__main__":
    demo()
