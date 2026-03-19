"""
Memory All Tasks
All tasks
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0))
    tasks = asyncio.all_tasks()
    await task
    print(len(tasks))


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
