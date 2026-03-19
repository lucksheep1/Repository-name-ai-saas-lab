"""
Memory Decorator
Decorator pattern for memory
"""
from memory import Memory


def logged(func):
    """Log decorator"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Completed {func.__name__}")
        return result
    return wrapper


def timed(func):
    """Time decorator"""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Took {time.time() - start:.2f}s")
        return result
    return wrapper


class DecoratedMemory:
    """Decorated memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    @logged
    @timed
    def add(self, content: str, **kwargs):
        return self.memory.add(content, **kwargs)
    
    @logged
    def search(self, query: str):
        return self.memory.search(query)


def demo():
    """Demo decorator"""
    memory = Memory(storage="json", path="./decorator_demo.json")
    decorated = DecoratedMemory(memory)
    
    decorated.add("Test")


if __name__ == "__main__":
    demo()
