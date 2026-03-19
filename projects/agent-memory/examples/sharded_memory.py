"""
Memory Sharding
Sharded memory storage
"""
from memory import Memory


class ShardedMemory:
    """Sharded memory"""
    
    def __init__(self, shards: int = 3):
        self.shards = shards
        self.memories = [Memory(storage="json", path=f"./shard_{i}.json") 
                        for i in range(shards)]
    
    def _shard(self, key: str) -> int:
        """Get shard"""
        return hash(key) % self.shards
    
    def add(self, content: str, **kwargs):
        """Add to shard"""
        shard = self._shard(content)
        return self.memories[shard].add(content, **kwargs)
    
    def search(self, query: str):
        """Search all shards"""
        results = []
        
        for mem in self.memories:
            results.extend(mem.search(query))
        
        return results
    
    def get_all(self):
        """Get all from all shards"""
        results = []
        
        for mem in self.memories:
            results.extend(mem.get_all())
        
        return results


def demo():
    """Demo sharding"""
    shard = ShardedMemory(2)
    
    shard.add("Test 1")
    shard.add("Test 2")
    
    print(f"Total: {len(shard.get_all())}")


if __name__ == "__main__":
    demo()
