"""
Memory Coroutine
Coroutine types
"""
from memory import Memory
from typing import Coroutine


async def coroutine_func() -> Coroutine:
    return "done"


def demo():
    import asyncio
    print(asyncio.run(coroutine_func()))


if __name__ == "__main__":
    demo()
