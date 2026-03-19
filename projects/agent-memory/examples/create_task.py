"""
Memory Create Task
Create task
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0))
    await task
    print("done")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
