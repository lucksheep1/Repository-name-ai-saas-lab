"""
Memory Middleware
Middleware for memory operations
"""
from agent_memory import Memory
from typing import Callable


class MemoryMiddleware:
    """Base middleware"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def before_add(self, content: str, kwargs: dict) -> tuple:
        """Called before add"""
        return content, kwargs
    
    def after_add(self, mem_id: str):
        """Called after add"""
        pass
    
    def before_search(self, query: str, kwargs: dict) -> tuple:
        """Called before search"""
        return query, kwargs
    
    def after_search(self, results: list):
        """Called after search"""
        pass


class LoggingMiddleware(MemoryMiddleware):
    """Log all operations"""
    
    def before_add(self, content: str, kwargs: dict) -> tuple:
        print(f"📝 Adding: {content[:30]}...")
        return content, kwargs
    
    def after_add(self, mem_id: str):
        print(f"   → Added: {mem_id}")
    
    def before_search(self, query: str, kwargs: dict) -> tuple:
        print(f"🔍 Searching: {query}")
        return query, kwargs
    
    def after_search(self, results: list):
        print(f"   → Found: {len(results)} results")


class ValidationMiddleware(MemoryMiddleware):
    """Validate content"""
    
    def before_add(self, content: str, kwargs: dict) -> tuple:
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        
        if len(content) > 10000:
            raise ValueError("Content too long")
        
        return content.strip(), kwargs


class MiddlewareChain:
    """Chain of middleware"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.middlewares = []
    
    def add(self, middleware: MemoryMiddleware):
        """Add middleware"""
        self.middlewares.append(middleware)
    
    def add_with_middleware(self, content: str, **kwargs):
        """Add with middleware chain"""
        # Before
        for mw in self.middlewares:
            content, kwargs = mw.before_add(content, kwargs)
        
        # Add
        mem_id = self.memory.add(content, **kwargs)
        
        # After
        for mw in self.middlewares:
            mw.after_add(mem_id)
        
        return mem_id
    
    def search_with_middleware(self, query: str, **kwargs):
        """Search with middleware chain"""
        # Before
        for mw in self.middlewares:
            query, kwargs = mw.before_search(query, kwargs)
        
        # Search
        results = self.memory.search(query, **kwargs)
        
        # After
        for mw in self.middlewares:
            mw.after_search(results)
        
        return results


def demo():
    """Demo middleware"""
    memory = Memory(storage="json", path="./middleware_demo.json")
    chain = MiddlewareChain(memory)
    
    print("=== Middleware Demo ===\n")
    
    # Add middleware
    chain.add(LoggingMiddleware(memory))
    chain.add(ValidationMiddleware(memory))
    
    # Add with middleware
    chain.add_with_middleware("Test memory")
    chain.add_with_middleware("Another test")
    
    print("\nSearch:")
    chain.search_with_middleware("test")
    
    # Cleanup
    import os
    if os.path.exists("./middleware_demo.json"):
        os.remove("./middleware_demo.json")


if __name__ == "__main__":
    demo()
