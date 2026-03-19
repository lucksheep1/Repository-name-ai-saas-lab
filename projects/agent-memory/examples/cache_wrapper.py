"""
Memory Cache Wrapper
Caching wrapper
"""
from agent_memory import Memory
import time


class CacheWrapper:
    """Cache wrapper"""
    
    def __init__(self, memory: Memory, ttl: int = 300):
        self.memory = memory
        self.ttl = ttl
        self.cache = {}
    
    def get(self, key: str):
        """Get from cache"""
        if key in self.cache:
            data, ts = self.cache[key]
            if time.time() - ts < self.ttl:
                return data
        
        return None
    
    def set(self, key: str, value):
        """Set cache"""
        self.cache[key] = (value, time.time())
    
    def search_cached(self, query: str):
        """Search with caching"""
        cache_key = f"search:{query}"
        
        result = self.get(cache_key)
        if result:
            return result
        
        result = self.memory.search(query)
        self.set(cache_key, result)
        
        return result


def demo():
    """Demo cache"""
    memory = Memory(storage="json", path="./cache_demo2.json")
    cache = CacheWrapper(memory)
    
    cache.search_cached("test")
    print("Cached search")
    
    import os
    if os.path.exists("./cache_demo2.json"):
        os.remove("./cache_demo2.json")


if __name__ == "__main__":
    demo()
