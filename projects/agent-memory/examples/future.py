"""
Memory Future
Async future
"""
from memory import Memory
import asyncio


async def main():
    memory = Memory(storage="json", path="future.json")
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, memory.add, "test")
    result = await future
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
