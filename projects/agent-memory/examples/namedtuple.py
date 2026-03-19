"""
Memory NamedTuple
Named tuple
"""
from memory import Memory
from collections import namedtuple


MemoryRecord = namedtuple("MemoryRecord", ["content", "tags", "created_at"])


def demo():
    record = MemoryRecord("Test", ["demo"], "2024-01-01")
    print(record)


if __name__ == "__main__":
    demo()
