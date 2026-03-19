"""
Memory Add Done Callback
Add done callback
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0))
    task.add_done_callback(lambda t: print("done"))
    await task


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
