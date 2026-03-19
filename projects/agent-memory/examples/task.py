"""
Memory Task
Async task
"""
from memory import Memory
import asyncio


async def task_func(memory):
    return memory.add("task")


async def main():
    memory = Memory(storage="json", path="task.json")
    task = asyncio.create_task(task_func(memory))
    result = await task
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
