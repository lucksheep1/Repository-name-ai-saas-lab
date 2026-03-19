"""
Memory Gather
Gather async
"""
from memory import Memory
import asyncio


async def add_async(memory, content):
    return memory.add(content)


async def main():
    memory = Memory(storage="json", path="gather.json")
    results = await asyncio.gather(
        add_async(memory, "test1"),
        add_async(memory, "test2"),
    )
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
