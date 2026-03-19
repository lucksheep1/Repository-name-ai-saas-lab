"""
Memory LRU Cache
LRU cache implementation
"""
from agent_memory import Memory


class LRUCache:
    """LRU cache"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key: str):
        """Get"""
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value):
        """Put"""
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
    
    def clear(self):
        """Clear"""
        self.cache.clear()
        self.order.clear()


def demo():
    """Demo LRU"""
    cache = LRUCache(capacity=3)
    
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    print(f"Get a: {cache.get('a')}")
    print(f"Get b: {cache.get('b')}")
    
    cache.put("d", 4)
    print(f"Get c: {cache.get('c')}")


if __name__ == "__main__":
    demo()
