"""
Memory Await
Await support
"""
from memory import Memory


async def slow_add(memory, content):
    import asyncio
    await asyncio.sleep(0.1)
    return memory.add(content)


def demo():
    import asyncio
    memory = Memory(storage="json", path="await.json")
    result = asyncio.run(slow_add(memory, "Test"))
    print(result)


if __name__ == "__main__":
    demo()
