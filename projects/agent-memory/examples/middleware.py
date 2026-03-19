"""
Memory Middleware
Middleware for memory operations
"""
from agent_memory import Memory


class MemoryMiddleware:
    """Base middleware class"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def on_add(self, content: str, kwargs: dict) -> tuple:
        """Called before add"""
        return content, kwargs
    
    def on_get(self, mem: dict) -> dict:
        """Called after get"""
        return mem
    
    def on_search(self, results: list) -> list:
        """Called after search"""
        return results


class LoggingMiddleware(MemoryMiddleware):
    """Log all operations"""
    
    def on_add(self, content: str, kwargs: dict):
        print(f"ADD: {content[:30]}...")
        return super().on_add(content, kwargs)
    
    def on_get(self, mem: dict):
        print(f"GET: {mem.get('id')}")
        return super().on_get(mem)


class UppercaseMiddleware(MemoryMiddleware):
    """Convert content to uppercase"""
    
    def on_add(self, content: str, kwargs: dict):
        return content.upper(), kwargs


class FilterMiddleware(MemoryMiddleware):
    """Filter content"""
    
    def __init__(self, memory: Memory, blocked: list = None):
        super().__init__(memory)
        self.blocked = blocked or ["bad", "ugly"]
    
    def on_add(self, content: str, kwargs: dict):
        for word in self.blocked:
            content = content.replace(word, "*" * len(word))
        return super().on_add(content, kwargs)


class MiddlewareChain:
    """Chain of middlewares"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.middlewares = []
    
    def use(self, middleware: MemoryMiddleware):
        """Add middleware"""
        self.middlewares.append(middleware)
    
    def add(self, content: str, **kwargs):
        """Add with middlewares"""
        for mw in self.middlewares:
            content, kwargs = mw.on_add(content, kwargs)
        
        return self.memory.add(content, **kwargs)


def demo():
    """Demo middleware"""
    memory = Memory(storage="json", path="./middleware_demo.json")
    chain = MiddlewareChain(memory)
    
    print("=== Memory Middleware Demo ===\n")
    
    # Add middlewares
    chain.use(LoggingMiddleware(memory))
    chain.use(UppercaseMiddleware(memory))
    chain.use(FilterMiddleware(memory))
    
    # Add (will go through all middlewares)
    chain.add("Hello world")
    chain.add("This is bad content")
    
    print("\nMemories:")
    for m in memory.get_all():
        print(f"  {m.get('content')}")
    
    # Cleanup
    import os
    if os.path.exists("./middleware_demo.json"):
        os.remove("./middleware_demo.json")


if __name__ == "__main__":
    demo()
