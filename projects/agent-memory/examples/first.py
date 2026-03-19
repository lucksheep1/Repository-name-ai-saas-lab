"""
Memory First
First completed
"""
from memory import Memory
import asyncio


async def fast():
    await asyncio.sleep(0.01)
    return "fast"


async def slow():
    await asyncio.sleep(1)
    return "slow"


async def main():
    done, pending = await asyncio.wait([fast(), slow()], return_when=asyncio.FIRST_COMPLETED)
    print(done.pop().result())


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
