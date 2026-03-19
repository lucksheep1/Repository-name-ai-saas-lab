"""
Memory Exception
Task exception
"""
from memory import Memory
import asyncio


async def fail():
    raise Exception("error")


async def main():
    task = asyncio.create_task(fail())
    try:
        await task
    except:
        print(task.exception())


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
