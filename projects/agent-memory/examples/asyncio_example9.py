"""
Memory asyncio_example9
asyncio_example9
"""
import asyncio


async def main():
    try:
        async with asyncio.timeout(0.1):
            await asyncio.sleep(1)
    except asyncio.TimeoutError:
        print("timeout")


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
