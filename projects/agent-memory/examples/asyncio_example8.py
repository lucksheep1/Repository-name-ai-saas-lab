"""
Memory asyncio_example8
asyncio_example8
"""
import asyncio


async def worker(n):
    await asyncio.sleep(0)
    return n * n


async def main():
    tasks = [worker(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
