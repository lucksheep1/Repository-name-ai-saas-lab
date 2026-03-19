"""
Memory REST Client
Client library for remote memory servers
"""
import requests
import json


class MemoryClient:
    """REST client for memory server"""
    
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"
    
    def add(self, content: str, tags: list = None, metadata: dict = None) -> dict:
        """Add memory"""
        data = {"content": content}
        
        if tags:
            data["tags"] = tags
        if metadata:
            data["metadata"] = metadata
        
        resp = self.session.post(f"{self.base_url}/memories", json=data)
        resp.raise_for_status()
        
        return resp.json()
    
    def search(self, query: str, limit: int = 10) -> list:
        """Search memories"""
        resp = self.session.get(
            f"{self.base_url}/memories/search",
            params={"q": query, "limit": limit}
        )
        resp.raise_for_status()
        
        return resp.json()
    
    def get(self, mem_id: str) -> dict:
        """Get memory by ID"""
        resp = self.session.get(f"{self.base_url}/memories/{mem_id}")
        resp.raise_for_status()
        
        return resp.json()
    
    def list(self, limit: int = 100) -> list:
        """List all memories"""
        resp = self.session.get(f"{self.base_url}/memories", params={"limit": limit})
        resp.raise_for_status()
        
        return resp.json()
    
    def delete(self, mem_id: str):
        """Delete memory"""
        resp = self.session.delete(f"{self.base_url}/memories/{mem_id}")
        resp.raise_for_status()


class CachedClient:
    """Client with local caching"""
    
    def __init__(self, client: MemoryClient, cache_ttl: int = 300):
        self.client = client
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def search(self, query: str, limit: int = 10) -> list:
        """Search with caching"""
        cache_key = f"search:{query}:{limit}"
        
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached
        
        results = self.client.search(query, limit)
        self.cache[cache_key] = (results, time.time())
        
        return results
    
    def invalidate(self):
        """Clear cache"""
        self.cache.clear()


import time


def demo():
    """Demo client"""
    print("=== Memory REST Client Demo ===\n")
    
    # This would connect to a real server
    # client = MemoryClient("http://localhost:5000", api_key="...")
    
    print("Usage:")
    print("""
# Create client
client = MemoryClient("http://localhost:5000", api_key="your_key")

# Add memory
mem = client.add("Hello world", tags=["greeting"])
print(f"Added: {mem['id']}")

# Search
results = client.search("hello")
for r in results:
    print(f"  {r['content']}")

# List all
all_mem = client.list()
print(f"Total: {len(all_mem)}")

# Delete
client.delete(mem['id'])
""")


if __name__ == "__main__":
    demo()
