"""
Memory Throw
Throw to task
"""
from memory import Memory
import asyncio


async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    task.throw(Exception("error"))


def demo():
    print("Throw ready")


if __name__ == "__main__":
    demo()
