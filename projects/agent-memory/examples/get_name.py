"""
Memory Get Name
Get task name
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0), name="my_task")
    print(task.get_name())


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
