"""
Memory Dataclass
Data class
"""
from memory import Memory
from dataclasses import dataclass


@dataclass
class MemoryData:
    content: str
    tags: list = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


def demo():
    data = MemoryData("Test", ["demo"])
    print(data)


if __name__ == "__main__":
    demo()
