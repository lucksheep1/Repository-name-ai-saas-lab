"""
Memory Ensure Future
Ensure future
"""
from memory import Memory
import asyncio


async def main():
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    future.set_result("done")
    print(await future)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
