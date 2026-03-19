"""
Memory Invalid State Error
Invalid state error
"""
from memory import Memory
import asyncio


def main():
    async def task():
        await asyncio.sleep(0)
    
    async def runner():
        t = asyncio.create_task(task())
        await t
        asyncio.create_task(task())
    
    try:
        asyncio.run(runner())
    except asyncio.InvalidStateError:
        print("InvalidStateError")


def demo():
    main()


if __name__ == "__main__":
    demo()
