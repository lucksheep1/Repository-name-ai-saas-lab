"""
Memory Timeout Error
Timeout error
"""
from memory import Memory
import asyncio


async def main():
    try:
        await asyncio.wait_for(asyncio.sleep(10), timeout=0.01)
    except asyncio.TimeoutError:
        print("Timeout")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
