"""
Memory CurrentTask
Current task
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.current_task()
    print(task.get_name())


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
