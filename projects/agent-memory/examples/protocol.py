"""
Memory Protocol
Protocol (structural subtyping)
"""
from memory import Memory
from typing import Protocol


class IMemory(Protocol):
    def add(self, content: str) -> str: ...
    def search(self, query: str): ...


def process_memory(mem: IMemory):
    mem.add("Test")


def demo():
    memory = Memory(storage="json", path="test.json")
    process_memory(memory)


if __name__ == "__main__":
    demo()
