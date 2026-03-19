"""
Memory Iterator Type
Iterator types
"""
from memory import Memory
from typing import Iterator


def iterate(memory: Memory) -> Iterator[str]:
    for mem in memory.get_all():
        yield mem.get("content", "")


def demo():
    print("Iterator ready")


if __name__ == "__main__":
    demo()
