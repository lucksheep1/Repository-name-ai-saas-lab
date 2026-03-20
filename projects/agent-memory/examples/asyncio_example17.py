"""
Memory asyncio_example17
asyncio_example17
"""
import asyncio


async def main():
    await asyncio.sleep(0.01)
    print("Done")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
