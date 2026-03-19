"""
Memory asyncio_example3
asyncio_example3
"""
import asyncio


async def task1():
    await asyncio.sleep(0.01)
    return "task1"


async def task2():
    await asyncio.sleep(0.01)
    return "task2"


async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
