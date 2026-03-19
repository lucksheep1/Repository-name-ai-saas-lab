"""
Memory Event Loop
Async event loop
"""
from memory import Memory
import asyncio


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    memory = Memory(storage="json", path="loop.json")
    result = loop.run_until_complete(asyncio.sleep(0))
    print(result)
    loop.close()


if __name__ == "__main__":
    main()
