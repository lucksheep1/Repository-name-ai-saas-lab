"""
Memory Semaphore
Semaphore async
"""
from memory import Memory
import asyncio


async def limited_add(sem, memory, content):
    async with sem:
        return memory.add(content)


async def main():
    memory = Memory(storage="json", path="sem.json")
    sem = asyncio.Semaphore(2)
    
    results = await asyncio.gather(
        limited_add(sem, memory, "test1"),
        limited_add(sem, memory, "test2"),
    )
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
