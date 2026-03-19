"""
Memory Run In Executor
Run in executor
"""
from memory import Memory
import asyncio
from concurrent.futures import ThreadPoolExecutor


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    def blocking_add(memory):
        return memory.add("test")
    
    memory = Memory(storage="json", path="executor.json")
    executor = ThreadPoolExecutor()
    
    future = loop.run_in_executor(executor, blocking_add, memory)
    result = loop.run_until_complete(future)
    print(result)
    
    executor.shutdown()
    loop.close()


def demo():
    main()


if __name__ == "__main__":
    demo()
