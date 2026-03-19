"""
Memory Remove Done Callback
Remove done callback
"""
from memory import Memory
import asyncio


def callback(t):
    print("done")


async def main():
    task = asyncio.create_task(asyncio.sleep(0))
    task.add_done_callback(callback)
    task.remove_done_callback(callback)
    await task


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
