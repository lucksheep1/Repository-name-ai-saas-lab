"""
Memory Cancel
Cancel task
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    task.cancel()
    print("cancelled")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
