"""
Memory Queue Async
Async queue
"""
from memory import Memory
import asyncio


async def producer(q, memory):
    await q.put(memory.add("item"))


async def consumer(q):
    item = await q.get()
    print(item)


async def main():
    q = asyncio.Queue()
    memory = Memory(storage="json", path="q.json")
    await asyncio.gather(producer(q, memory), consumer(q))


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
