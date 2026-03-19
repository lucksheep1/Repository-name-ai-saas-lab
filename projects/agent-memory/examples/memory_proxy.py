"""
Memory Proxy
Proxy pattern for memory
"""
from memory import Memory


class ProxyMemory:
    """Proxy for memory"""
    
    def __init__(self, real: Memory):
        self.real = real
        self.cache = {}
    
    def add(self, content: str, **kwargs):
        self.cache.clear()
        return self.real.add(content, **kwargs)
    
    def search(self, query: str):
        if query in self.cache:
            return self.cache[query]
        
        results = self.real.search(query)
        self.cache[query] = results
        return results


def demo():
    real = Memory(storage="json", path="./proxy_real.json")
    proxy = ProxyMemory(real)
    
    proxy.add("Test")
    print(f"Search: {len(proxy.search('test'))}")


if __name__ == "__main__":
    demo()
