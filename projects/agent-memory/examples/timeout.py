"""
Memory Timeout
Async timeout
"""
from memory import Memory
import asyncio


async def slow_add(memory):
    await asyncio.sleep(10)
    return memory.add("test")


async def main():
    memory = Memory(storage="json", path="timeout.json")
    try:
        result = await asyncio.wait_for(slow_add(memory), timeout=0.1)
        print(result)
    except asyncio.TimeoutError:
        print("Timeout")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
