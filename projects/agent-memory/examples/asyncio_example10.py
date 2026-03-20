"""
Memory asyncio_example10
asyncio_example10
"""
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(0.1))
    print(task)


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
