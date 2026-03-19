"""
Memory Cache
Caching layer
"""
from memory import Memory


class Cache:
    def __init__(self):
        self.store = {}
    
    def get(self, key: str):
        return self.store.get(key)
    
    def set(self, key: str, value):
        self.store[key] = value
    
    def delete(self, key: str):
        if key in self.store:
            del self.store[key]
    
    def clear(self):
        self.store.clear()


def demo():
    cache = Cache()
    cache.set("key", "value")
    print(cache.get("key"))


if __name__ == "__main__":
    demo()
