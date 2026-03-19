"""
Memory Wait For
Wait for
"""
from memory import Memory
import asyncio


async def main():
    result = await asyncio.wait_for(asyncio.sleep(0.01), timeout=1)
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
