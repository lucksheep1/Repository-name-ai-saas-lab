"""
Memory Set Loop
Set event loop
"""
from memory import Memory
import asyncio


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print(loop)
    loop.close()


def demo():
    main()


if __name__ == "__main__":
    demo()
