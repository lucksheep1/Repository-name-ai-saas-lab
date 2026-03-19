"""
Caching Layer for Memory
Speed up repeated queries with intelligent caching
"""
from agent_memory import Memory
import time
from functools import wraps
from typing import Any, Callable


class CachedMemory:
    """Memory with caching layer for faster repeated queries"""
    
    def __init__(self, memory: Memory, ttl: int = 300):
        self.memory = memory
        self.ttl = ttl  # Cache TTL in seconds
        self.cache = {}  # {query: (timestamp, results)}
    
    def _is_valid(self, entry: tuple) -> bool:
        """Check if cache entry is still valid"""
        timestamp, _ = entry
        return (time.time() - timestamp) < self.ttl
    
    def search(self, query: str, limit: int = 10, use_cache: bool = True):
        """Search with caching"""
        cache_key = f"search:{query}:{limit}"
        
        if use_cache and cache_key in self.cache:
            entry = self.cache[cache_key]
            if self._is_valid(entry):
                print(f"⚡ Cache hit for: {query}")
                return entry[1]
            else:
                del self.cache[cache_key]
        
        # Cache miss - execute query
        results = self.memory.search(query, limit=limit)
        
        # Store in cache
        self.cache[cache_key] = (time.time(), results)
        
        return results
    
    def get_all(self, use_cache: bool = True):
        """Get all with caching"""
        cache_key = "get_all"
        
        if use_cache and cache_key in self.cache:
            entry = self.cache[cache_key]
            if self._is_valid(entry):
                return entry[1]
        
        results = self.memory.get_all()
        self.cache[cache_key] = (time.time(), results)
        return results
    
    def invalidate(self, pattern: str = None):
        """Invalidate cache"""
        if pattern:
            # Invalidate matching keys
            keys_to_delete = [k for k in self.cache if pattern in k]
            for k in keys_to_delete:
                del self.cache[k]
        else:
            # Clear all
            self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        now = time.time()
        valid = sum(1 for e in self.cache.values() if self._is_valid(e))
        
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid,
            "expired_entries": len(self.cache) - valid,
            "ttl_seconds": self.ttl,
        }


def cached_search(memory: Memory, ttl: int = 300):
    """Decorator for cached search"""
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(query: str, *args, **kwargs):
            cache_key = f"{func.__name__}:{query}:{str(args)}:{str(kwargs)}"
            
            if cache_key in cache:
                timestamp, result = cache[cache_key]
                if (time.time() - timestamp) < ttl:
                    return result
            
            result = func(query, *args, **kwargs)
            cache[cache_key] = (time.time(), result)
            return result
        
        wrapper.cache = cache
        return wrapper
    
    return decorator


class MemoryCache:
    """LRU cache for memory queries"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
    
    def get(self, key: str) -> Any:
        """Get from cache"""
        if key not in self.cache:
            return None
        
        # Update access order (move to end)
        self.access_order.remove(key)
        self.access_order.append(key)
        
        return self.cache[key][1]
    
    def set(self, key: str, value: Any):
        """Set cache entry"""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Evict oldest
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = (time.time(), value)
        self.access_order.append(key)
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_order.clear()


def demo():
    """Demo caching"""
    memory = Memory(storage="json", path="./cache_demo.json")
    
    # Add some memories
    memory.add("Python is great for AI")
    memory.add("FastAPI is fast")
    memory.add("SQLite is lightweight")
    memory.add("Memory is important for agents")
    
    cached = CachedMemory(memory, ttl=60)
    
    print("=== Cached Memory Demo ===\n")
    
    # First search (cache miss)
    print("First search:")
    results1 = cached.search("python")
    print(f"Found: {len(results1)} results\n")
    
    # Second search (cache hit)
    print("Second search:")
    results2 = cached.search("python")
    print(f"Found: {len(results2)} results\n")
    
    # Stats
    stats = cached.get_stats()
    print(f"Cache stats: {stats}")
    
    # Cleanup
    import os
    if os.path.exists("./cache_demo.json"):
        os.remove("./cache_demo.json")


if __name__ == "__main__":
    demo()
