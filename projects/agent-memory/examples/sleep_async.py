"""
Memory Sleep
Async sleep
"""
from memory import Memory
import asyncio


async def main():
    await asyncio.sleep(0.01)
    memory = Memory(storage="json", path="sleep.json")
    print(memory.add("test"))


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
