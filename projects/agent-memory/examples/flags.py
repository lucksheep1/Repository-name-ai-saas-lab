"""
Memory Flags
Flags pattern
"""
from memory import Memory
from flags import Flags, auto


class MemoryFlags(Flags):
    READONLY = auto()
    CACHED = auto()
    COMPRESSED = auto()


def demo():
    flags = MemoryFlags.READONLY | MemoryFlags.CACHED
    print(flags)


if __name__ == "__main__":
    demo()
