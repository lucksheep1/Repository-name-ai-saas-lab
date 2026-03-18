#!/usr/bin/env python3
"""
Agent Memory - Cached Memory
=============================
Memory with caching layer for faster repeated queries.

Usage:
    from cached_memory import CachedMemory
    
    memory = CachedMemory(storage="json", path="./memory.json")
    # First search - from storage
    results = memory.search("query")
    # Second search - from cache
    results = memory.search("query")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import hashlib
from typing import List, Dict, Optional, Any
from agent_memory import Memory


class CacheEntry:
    """Cache entry with TTL."""
    def __init__(self, value: Any, ttl: int = 300):
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
    
    def is_valid(self) -> bool:
        """Check if entry is still valid."""
        return time.time() - self.created_at < self.ttl


class CachedMemory(Memory):
    """Memory with caching layer."""
    
    def __init__(self, *args, cache_ttl: int = 300, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_ttl = cache_ttl
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _make_key(self, method: str, *args, **kwargs) -> str:
        """Create cache key."""
        key_data = f"{method}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached value."""
        if key in self.cache:
            entry = self.cache[key]
            if entry.is_valid():
                self.cache_hits += 1
                return entry.value
            else:
                del self.cache[key]
        self.cache_misses += 1
        return None
    
    def _set_cached(self, key: str, value: Any):
        """Set cached value."""
        self.cache[key] = CacheEntry(value, self.cache_ttl)
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search with caching."""
        key = self._make_key("search", query, top_k)
        
        cached = self._get_cached(key)
        if cached is not None:
            return cached
        
        result = super().search(query, top_k)
        self._set_cached(key, result)
        return result
    
    def get_context(self, max_tokens: int = 2000, max_memories: int = 10) -> str:
        """Get context with caching."""
        key = self._make_key("get_context", max_tokens, max_memories)
        
        cached = self._get_cached(key)
        if cached is not None:
            return cached
        
        result = super().get_context(max_tokens, max_memories)
        self._set_cached(key, result)
        return result
    
    def get_recent(self, limit: int = 10) -> List[dict]:
        """Get recent with caching."""
        key = self._make_key("get_recent", limit)
        
        cached = self._get_cached(key)
        if cached is not None:
            return cached
        
        result = super().get_recent(limit)
        self._set_cached(key, result)
        return result
    
    def get_timeline(self, limit: int = 20) -> List[dict]:
        """Get timeline with caching."""
        key = self._make_key("get_timeline", limit)
        
        cached = self._get_cached(key)
        if cached is not None:
            return cached
        
        result = super().get_timeline(limit)
        self._set_cached(key, result)
        return result
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory and invalidate cache."""
        result = super().add(text, metadata, ttl_days)
        self.invalidate_cache()
        return result
    
    def delete(self, memory_id: str) -> bool:
        """Delete memory and invalidate cache."""
        result = super().delete(memory_id)
        if result:
            self.invalidate_cache()
        return result
    
    def clear(self):
        """Clear memory and cache."""
        super().clear()
        self.cache.clear()
    
    def invalidate_cache(self):
        """Invalidate all cache."""
        self.cache.clear()
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "cached_entries": len(self.cache)
        }


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "cached_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Cached Memory Demo")
    print("=" * 50)
    
    # Create cached memory
    memory = CachedMemory(storage="json", path=demo_path, cache_ttl=60)
    
    # Add some memories
    print("\n1. Adding memories...")
    memory.add("User likes coffee")
    memory.add("User prefers dark mode")
    memory.add("User is a developer")
    
    # First search - cache miss
    print("\n2. First search (cache miss)...")
    results1 = memory.search("user")
    print(f"   Found: {len(results1)} results")
    print(f"   Stats: {memory.get_cache_stats()}")
    
    # Second search - cache hit
    print("\n3. Second search (cache hit)...")
    results2 = memory.search("user")
    print(f"   Found: {len(results2)} results")
    print(f"   Stats: {memory.get_cache_stats()}")
    
    # Third search - cache hit
    print("\n4. Third search (cache hit)...")
    results3 = memory.search("user")
    print(f"   Found: {len(results3)} results")
    print(f"   Stats: {memory.get_cache_stats()}")
    
    # Add new memory - invalidate cache
    print("\n5. Adding new memory (invalidates cache)...")
    memory.add("User loves Python")
    print(f"   Stats: {memory.get_cache_stats()}")
    
    # Search again - cache miss
    print("\n6. Search after add (cache miss)...")
    results4 = memory.search("user")
    print(f"   Found: {len(results4)} results")
    print(f"   Stats: {memory.get_cache_stats()}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
