"""
Memory Lock Async
Async lock
"""
from memory import Memory
import asyncio


async def main():
    lock = asyncio.Lock()
    async with lock:
        print("Locked")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
