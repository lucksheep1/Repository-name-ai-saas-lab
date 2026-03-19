"""
Memory asyncio_example7
asyncio_example7
"""
import asyncio


async def main():
    async with asyncio.timeout(1):
        await asyncio.sleep(0.1)
        print("completed")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
