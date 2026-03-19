"""
Memory As Completed
As completed
"""
from memory import Memory
import asyncio


async def task(n):
    await asyncio.sleep(n / 10)
    return n


async def main():
    results = []
    for coro in asyncio.as_completed([task(i) for i in range(5)]):
        result = await coro
        results.append(result)
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
