"""
Memory Awaitable
Awaitable types
"""
from memory import Memory
from typing import Awaitable


async def async_func() -> str:
    return "done"


def process_awaitable(aw: Awaitable[str]) -> str:
    import asyncio
    return asyncio.run(aw)


def demo():
    print(process_awaitable(async_func()))


if __name__ == "__main__":
    demo()
