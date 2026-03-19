"""
Memory Async
Async support
"""
from memory import Memory
import asyncio


async def async_add(memory, content):
    return memory.add(content)


async def main():
    memory = Memory(storage="json", path="async.json")
    result = await async_add(memory, "Test")
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
