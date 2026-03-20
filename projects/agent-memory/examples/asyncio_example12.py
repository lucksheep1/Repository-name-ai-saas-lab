"""
Memory asyncio_example12
asyncio_example12
"""
import asyncio


async def main():
    await asyncio.sleep(0.01)
    print("async done")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
