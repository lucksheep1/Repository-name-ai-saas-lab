"""
Memory Pool
Object pool for memory
"""
from memory import Memory


class PooledMemory:
    """Pooled memory"""
    def __init__(self):
        self.pool = []
        self.in_use = set()
    
    def acquire(self) -> Memory:
        if self.pool:
            mem = self.pool.pop()
        else:
            mem = Memory(storage="json", path=f"./pool_{len(self.in_use)}.json")
        
        self.in_use.add(id(mem))
        return mem
    
    def release(self, mem: Memory):
        self.in_use.discard(id(mem))
        self.pool.append(mem)


def demo():
    pool = PooledMemory()
    
    mem = pool.acquire()
    mem.add("Test")
    print(f"Count: {len(mem.get_all())}")
    
    pool.release(mem)


if __name__ == "__main__":
    demo()
