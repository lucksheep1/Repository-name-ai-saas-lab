"""
Memory AsyncGenerator
Async generator
"""
from memory import Memory
from typing import AsyncGenerator


async def async_gen(memory) -> AsyncGenerator[str, None]:
    for mem in memory.get_all():
        yield mem.get("content", "")


def demo():
    print("Async generator ready")


if __name__ == "__main__":
    demo()
