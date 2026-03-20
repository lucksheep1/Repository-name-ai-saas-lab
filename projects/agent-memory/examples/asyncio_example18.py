"""
Memory asyncio_example18
asyncio_example18
"""
import asyncio


async def fetch(url):
    return url


async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"))
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
