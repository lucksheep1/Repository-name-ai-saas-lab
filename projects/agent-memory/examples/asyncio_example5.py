"""
Memory asyncio_example5
asyncio_example5
"""
import asyncio


async def fetch(url):
    return f"data from {url}"


async def main():
    tasks = [fetch(f"url{i}") for i in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
