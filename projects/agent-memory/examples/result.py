"""
Memory Result
Task result
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0))
    await task
    print(task.result())


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
