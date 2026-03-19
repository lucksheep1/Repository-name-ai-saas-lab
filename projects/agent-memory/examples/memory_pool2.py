"""
Memory Pool
Connection pool
"""
from memory import Memory


class Pool:
    def __init__(self, factory, size: int = 5):
        self.factory = factory
        self.size = size
        self.available = []
        self.in_use = set()
    
    def acquire(self):
        if self.available:
            mem = self.available.pop()
        else:
            mem = self.factory()
        
        self.in_use.add(id(mem))
        return mem
    
    def release(self, mem):
        self.in_use.discard(id(mem))
        if len(self.available) < self.size:
            self.available.append(mem)


def demo():
    pool = Pool(lambda: Memory(storage="json", path="test.json"))
    mem = pool.acquire()
    pool.release(mem)
    print("Pool demo done")


if __name__ == "__main__":
    demo()
