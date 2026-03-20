"""
Memory asyncio_example14
asyncio_example14
"""
import asyncio


async def task(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"


async def main():
    results = await asyncio.gather(
        task("A", 0.1),
        task("B", 0.05),
        task("C", 0.15)
    )
    for r in results:
        print(r)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
