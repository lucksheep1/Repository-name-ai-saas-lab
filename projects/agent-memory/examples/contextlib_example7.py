"""
Memory contextlib_example7
contextlib_example7
"""
from contextlib import asynccontextmanager


@asynccontextmanager
async def my_async_context():
    print("enter")
    yield
    print("exit")


async def demo():
    async with my_async_context():
        print("inside")


def main():
    import asyncio
    asyncio.run(demo())


if __name__ == "__main__":
    main()
