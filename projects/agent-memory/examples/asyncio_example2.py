"""
Memory asyncio_example2
asyncio_example2
"""
import asyncio


async def fetch_data():
    await asyncio.sleep(0.01)
    return "data"


async def main():
    result = await fetch_data()
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
