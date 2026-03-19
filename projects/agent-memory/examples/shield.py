"""
Memory Shield
Async shield
"""
from memory import Memory
import asyncio


async def main():
    try:
        await asyncio.shield(asyncio.sleep(0))
    except Exception as e:
        print(e)
    print("shielded")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
