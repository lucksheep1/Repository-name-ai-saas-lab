"""
Memory Await
Await in async
"""
from memory import Memory
import asyncio


async def main():
    memory = Memory(storage="json", path="await_demo.json")
    task = asyncio.create_task(asyncio.to_thread(memory.add, "Test"))
    await task
    print("Done")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
