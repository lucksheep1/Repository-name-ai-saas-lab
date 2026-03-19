"""
Memory Broken Barrier Error
Broken barrier error
"""
from memory import Memory
import asyncio


async def worker(barrier):
    await barrier.wait()
    print("done")


async def main():
    barrier = asyncio.Barrier(2)
    try:
        await asyncio.gather(worker(barrier), worker(barrier))
    except asyncio.BrokenBarrierError:
        print("Broken")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
