"""
Memory asyncio_example4
asyncio_example4
"""
import asyncio


async def demo():
    await asyncio.sleep(0)
    print("async done")


def main():
    asyncio.run(demo())


if __name__ == "__main__":
    main()
