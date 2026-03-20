"""
Memory asyncio_example13
asyncio_example13
"""
import asyncio


async def fetch_data():
    await asyncio.sleep(0.1)
    return "data"


async def main():
    result = await fetch_data()
    print(result)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
