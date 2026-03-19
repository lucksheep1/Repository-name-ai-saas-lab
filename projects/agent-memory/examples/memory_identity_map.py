"""
Memory Identity Map
Identity Map pattern
"""
from memory import Memory


class IdentityMap:
    def __init__(self):
        self.map = {}
    
    def get(self, key: str):
        return self.map.get(key)
    
    def set(self, key: str, value):
        self.map[key] = value
    
    def clear(self):
        self.map.clear()


class MemoryWithIdentity:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.identity = IdentityMap()
    
    def get(self, mem_id: str):
        cached = self.identity.get(mem_id)
        if cached:
            return cached
        
        mem = self.memory.get(mem_id)
        if mem:
            self.identity.set(mem_id, mem)
        
        return mem


def demo():
    memory = Memory(storage="json", path="./identity_demo.json")
    mem_with_id = MemoryWithIdentity(memory)
    
    mem_id = memory.add("Test")
    
    m1 = mem_with_id.get(mem_id)
    m2 = mem_with_id.get(mem_id)
    
    print(f"Same: {m1 is m2}")


if __name__ == "__main__":
    demo()
