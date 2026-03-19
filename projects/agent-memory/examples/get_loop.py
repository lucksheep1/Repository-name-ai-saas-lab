"""
Memory Get Loop
Get event loop
"""
from memory import Memory
import asyncio


async def main():
    loop = asyncio.get_event_loop()
    print(loop)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
