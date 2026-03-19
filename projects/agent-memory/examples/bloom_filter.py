"""
Memory Bloom Filter
Bloom filter for deduplication
"""
from memory import Memory


class BloomFilter:
    """Bloom filter"""
    
    def __init__(self, size: int = 1000):
        self.size = size
        self.array = [False] * size
    
    def _hash(self, item: str) -> int:
        """Hash function"""
        import hashlib
        return int(hashlib.md5(item.encode()).hexdigest(), 16) % self.size
    
    def add(self, item: str):
        """Add"""
        idx = self._hash(item)
        self.array[idx] = True
    
    def contains(self, item: str) -> bool:
        """Check"""
        idx = self._hash(item)
        return self.array[idx]


def demo():
    """Demo bloom"""
    bf = BloomFilter()
    
    bf.add("test")
    print(f"Contains test: {bf.contains('test')}")
    print(f"Contains other: {bf.contains('other')}")


if __name__ == "__main__":
    demo()
