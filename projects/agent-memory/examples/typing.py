"""
Memory Type
Type hints
"""
from memory import Memory
from typing import List, Optional


def add_memory(mem: Memory, content: str, tags: Optional[List[str]] = None) -> str:
    return mem.add(content, tags=tags or [])


def demo():
    memory = Memory(storage="json", path="test.json")
    print(add_memory(memory, "Test"))


if __name__ == "__main__":
    demo()
