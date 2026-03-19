"""
Memory New Event Loop
New event loop
"""
from memory import Memory
import asyncio


def main():
    loop = asyncio.new_event_loop()
    print(loop)
    loop.close()


def demo():
    main()


if __name__ == "__main__":
    demo()
