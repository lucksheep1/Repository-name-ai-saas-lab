"""
Memory AsyncIterator
Async iterator
"""
from memory import Memory
from typing import AsyncIterator


async def async_iterate(memory) -> AsyncIterator[str]:
    for mem in memory.get_all():
        yield mem.get("content", "")


def demo():
    print("Async iterator ready")


if __name__ == "__main__":
    demo()
