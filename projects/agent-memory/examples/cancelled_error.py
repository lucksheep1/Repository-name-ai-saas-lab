"""
Memory Cancelled Error
Cancelled error
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Cancelled")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
