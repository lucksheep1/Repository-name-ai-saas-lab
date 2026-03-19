"""
Memory dataclasses
dataclasses utilities
"""
from memory import Memory
from dataclasses import dataclass, field


@dataclass
class MemoryItem:
    content: str
    tags: list = field(default_factory=list)


def demo():
    item = MemoryItem("test", ["tag"])
    print(item)


if __name__ == "__main__":
    demo()
