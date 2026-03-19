"""
Memory Enum
Enumeration
"""
from memory import Memory
from enum import Enum, auto


class StorageType(Enum):
    JSON = auto()
    SQLITE = auto()
    FAISS = auto()


def demo():
    print(StorageType.JSON)


if __name__ == "__main__":
    demo()
