"""
Memory asyncio_example15
asyncio_example15
"""
import asyncio


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(asyncio.sleep(0.1, result="A"))
        tg.create_task(asyncio.sleep(0.05, result="B"))


def demo():
    asyncio.run(main())


if __name__ == "__main__":
    demo()
